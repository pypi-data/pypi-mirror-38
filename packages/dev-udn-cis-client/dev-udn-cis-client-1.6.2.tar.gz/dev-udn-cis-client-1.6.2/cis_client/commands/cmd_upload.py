from __future__ import unicode_literals

import os
import stat
import copy

from concurrent import futures
import click
import retrying

from cis_client import cli
from cis_client.commands import utils
from cis_client.lib.cis_gateway import http_upload_client
from cis_client.lib.cis_gateway import aspera_client
from cis_client.lib.cis_gateway import sftp_client
from cis_client.lib.cis_north import content_client
from cis_client import exception


@click.command('upload', context_settings=utils.CONTEXT_SETTINGS, help=
               'Uploads content via HTTP/Aspera/SFTP.')
@click.option('--protocol', type=click.Choice(['http', 'aspera', 'sftp']), default='http', show_default=True,
              help='Protocol for loading. Can be http, aspera or sftp.')
@click.option('--ingest-point', required=True, type=click.STRING,
              help='Ingest point to load content to.')
@click.option('--source-file-list', type=click.Path(resolve_path=True),
              help='Path to file that contains list of full source paths to content separated by new line symbol. '
                   'Files from the list will be uploaded.')
@click.option('--source-file', type=click.STRING,
              help='Comma separated list of full source paths to content that will be uploaded. '
                   'Can contain path to directory with files if upload protocol is aspera.')
@click.option('--skip-errors', type=click.BOOL, default=False, show_default=True, is_flag=True,
              help='Continue upload other files if some file upload was failed.')
@click.option('--verify-checksum', type=click.BOOL, default=False, show_default=True, is_flag=True,
              help='Verify md5 checksum of uploaded file.')
@click.option('--destination-path', type=click.STRING,
              help='Destination path. '
                   'Can be directory like dir1/dir2/. If value ends with / destination '
                   'file path will be composed from this value + source filename. '
                   'If this value doesn\'t end with / so destination path will be the same.'
                   'In case when full destination path is specified input path list can contain only one input file.')
@click.option('--overwrite', type=click.Choice(['no', 'ask', 'all']), default='no', show_default=True,
               help='Overwrites files if file exists on remote storage. "ask" means ask each time before overwriting.')
@click.option('--max-transfer-rate', type=click.STRING, default='1G', show_default=True,
              help='Aspera max transfer rate. For example 10G, 100m')
@click.option('--threads', type=click.IntRange(1, 32), default=1, show_default=True,
              help='Count of threads. Each thread uploads separate file.')
@utils.add_host_options
@utils.add_auth_options
@utils.add_credentials_options
@cli.pass_context
@utils.handle_exceptions
@utils.check_cis_version
def cli(ctx, **kwargs):
    paths = utils.get_source_file_list_from_kwargs(**kwargs)
    north_host = kwargs.pop('north_host')
    ingest_point = kwargs.pop('ingest_point')
    destination_path = kwargs.pop('destination_path')
    skip_errors = kwargs.pop('skip_errors')
    max_transfer_rate = kwargs.pop('max_transfer_rate')
    overwrite = kwargs.pop('overwrite')
    verify_checksum = kwargs.pop('verify_checksum')
    threads = kwargs.pop('threads')
    if overwrite == 'ask' and threads > 1:  # for single thread only
        raise exception.OptionException(
            "Option '--overwrite=ask' can not be used with option --thread > 1.")
    if destination_path and len(destination_path.split(',')) > 1:
        raise exception.OptionException(
            "Option --destination-path can contain only one path: "
            "directory with '/' suffix or full destination path for single source file.")
    if (destination_path and not destination_path.endswith('/') and
            len(paths) != 1):
        raise exception.OptionException(
            "To upload several files you need to specify destination directory in "
            "--destination-path option. Directory must contain suffix '/'. "
            'For example --destination-path "{}"/'.format(destination_path))

    checksum_calculator = utils.ChecksumCalculator()
    auth_keeper = utils.AuthKeeper(north_host=north_host, ingest_point=ingest_point, **kwargs)
    from cis_client.lib.cis_north import ingest_point_client
    ingest_point_client = ingest_point_client.IngestPointClient(north_host, insecure=kwargs['insecure'])
    ingest_point_info = ingest_point_client.get(auth_keeper.get_token(), ingest_point, **kwargs)
    try:
        with futures.ThreadPoolExecutor(max_workers=threads) as executor:
            future_list = [
                executor.submit(upload_single_file, path, kwargs, destination_path, north_host, ingest_point,
                                overwrite, max_transfer_rate, verify_checksum, skip_errors, checksum_calculator,
                                auth_keeper, ingest_point_info, threads)
                for path in paths
            ]
            for future in futures.as_completed(future_list):
                future.result()

    finally:
        path_list = checksum_calculator.full_dst_path_2_path.keys()
        if verify_checksum and path_list:
            utils.display('Check/wait that all md5sum related jobs are done.')
            utils.wait_job_done(north_host, path_list, **kwargs)
            checksum_calculator.join()
            for full_dst_path in checksum_calculator.full_dst_path_2_path:
                content_info = content_client.get_content(
                    north_host, ingest_point, full_dst_path,
                    checksum='md5', token=auth_keeper.get_token(), **kwargs)
                remote_file_md5sum = content_info.get('checksum', {}).get('md5')
                local_file_md5sum = checksum_calculator.get_md5(full_dst_path)
                if remote_file_md5sum != local_file_md5sum:
                    utils.display("md5sum doens't match for \"{}\".".format(full_dst_path))
                else:
                    utils.display("md5sum verified for \"{}\".".format(full_dst_path))


def upload_single_file(path, kwargs, destination_path, north_host, ingest_point, overwrite,
                       max_transfer_rate, verify_checksum, skip_errors, checksum_calculator,
                       auth_keeper, ingest_point_info, threads):
    if destination_path:
        if destination_path.endswith('/'):
            full_dst_path = ''.join([destination_path, os.path.basename(path)])
        else:
            full_dst_path = destination_path
    else:
        full_dst_path = os.path.basename(path)
    utils.display('Uploading "{}" ... to "{}"'.format(path, full_dst_path))
    try:
        @retrying.retry(wait_random_min=100, wait_random_max=1000, stop_max_attempt_number=3)
        def _upload_single_file():
            kwargs_per_upload = copy.deepcopy(kwargs)
            # check if file already uploaded
            stat_info = os.stat(path)
            if stat.S_ISDIR(stat_info.st_mode):
                utils.display('Skip to upload directory "{}"'.format(path))
                return
            content_info = None
            try:
                content_info = content_client.get_content(
                    north_host, ingest_point, full_dst_path, token=auth_keeper.get_token(),
                    context=kwargs_per_upload, checksum='md5', **kwargs_per_upload)
                if content_info['stat']['type'] == 'directory':
                    raise exception.UploadDirConflictException(full_dst_path)
                if (content_info['stat']['type'] == 'file' and
                            content_info['stat']['size'] == stat_info.st_size and
                            content_info.get('checksum', {}).get('md5') == utils.md5(path)):
                    utils.display('File "{}" is already present on "{}"'.format(
                        path, full_dst_path))
                    return
            except exception.HttpClientError as e:
                if e.response.status_code != 404:
                    raise

            if content_info and overwrite == 'no':  # add no-skip and rename this one to no-raise
                raise exception.UploadConflictException(full_dst_path)
            if content_info and overwrite == 'ask':  # for single thread only
                if not click.confirm('File "{}" exists on remote server. Do you want to overwrite it?'.format(
                        full_dst_path)):
                    utils.display('Skipping to upload "{}" file.'.format(path))
                    return
            if kwargs_per_upload['protocol'] == 'aspera':
                separate_output = bool(threads > 1)
                aspera_client.aspera_upload(
                    ingest_point_info, auth_keeper.get_access_key(), path, destination_path=full_dst_path,
                    max_transfer_rate=max_transfer_rate, separate_output=separate_output, **kwargs_per_upload)
            else:
                total_size = os.path.getsize(path)

                def progress_upload(progress_bar, ingest_point_info, access_key, path, full_dst_path,
                                    content_info, **kwargs_per_upload):
                    if kwargs_per_upload['protocol'] == 'http':
                        response = http_upload_client.http_upload(
                            ingest_point_info, access_key, path, destination_path=full_dst_path,
                            progress_callback=lambda transferred: progress_bar.update(transferred) if threads == 1 else None,
                            overwrite=content_info is not None,
                            **kwargs_per_upload)
                    elif kwargs_per_upload['protocol'] == 'sftp':
                        response = sftp_client.sftp_upload(
                            ingest_point_info, access_key, path, destination_path=full_dst_path,
                            progress_callback=lambda transferred, whole: progress_bar.update(transferred) if threads == 1 else None,
                            overwrite=content_info is not None,
                            **kwargs_per_upload)
                    return response

                if threads == 1:  # draw of progress bar with mixed prints works with single thread only
                    with utils.ProgressBar(max_value=total_size) as progress_bar:
                        response = progress_upload(
                            progress_bar, ingest_point_info, auth_keeper.get_access_key(), path, full_dst_path,
                            content_info, **kwargs_per_upload)
                else:
                    response = progress_upload(
                        None, ingest_point_info, auth_keeper.get_access_key(), path, full_dst_path,
                        content_info, **kwargs_per_upload)
            utils.display('File "{}" was successfully uploaded to "{}"'.format(path, full_dst_path))
            if verify_checksum:
                checksum_calculator.md5sum(path, full_dst_path)

        _upload_single_file()
    except Exception as e:
        if skip_errors:
            with utils.handle_exceptions_contextmanager(reraise=False, exit_on_exception=False):
                raise
        else:
            raise
