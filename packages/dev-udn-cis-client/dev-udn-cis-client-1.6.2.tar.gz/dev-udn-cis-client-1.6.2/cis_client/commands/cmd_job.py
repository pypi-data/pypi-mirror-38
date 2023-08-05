from __future__ import unicode_literals

import collections
from builtins import str as text

import click

from cis_client import cli
from cis_client.commands import utils
from cis_client.lib.cis_north import jobs_client
from cis_client import exception
from cis_client.commands import printer
from cis_client.commands import utils


job_datetime_fields = (
    'created_at',
    'started_at',
    'ready_at',
    'last_response_at',
    'finished_at',
    'next_stop_at',
    'next_start_at'
)


@click.group(help='Job management.')
def job_cli():
    pass


@job_cli.command('list', context_settings=utils.CONTEXT_SETTINGS, help='Lists jobs.')
@click.option('--ingest-point', type=click.STRING,
              help='Ingest point')
@click.option('--path-list-file', type=click.Path(resolve_path=True),
              help='Path to file that contains list of full paths to content separated by new line symbol.')
@click.option('--destination-path', type=click.STRING,
              help='Comma separated list of full paths to content.')
@click.option('--job-type', type=click.STRING,
              help='Job type like "abr" or "http-push" or "abr,http-push" or other')
@click.option('--state', type=click.STRING,
              help='an integer representation of composited states: pending, ready, scheduling, starting, '
                   'running, suspending, pausing, resuming, cancelling, completed, suspended, paused, failed, '
                   'cancelled, done. General purpose - for debugging.')
@click.option('--state-simple', type=click.STRING,
              help='Human readable status. Can contain values: "pending", "running", "cancelling", '
                   '"paused", "completed", "failed" in job query response.')
@click.option('--aggregated-status', type=click.STRING,
              help='Aggregated status. Can contain values: "uploading", "processing", "local_done", '
                   '"global_done", "failed".')
@click.option('--latest', type=click.BOOL, default=False, show_default=True, is_flag=True,
              help='Boolean. If true shows only the latest job related to specific filename and type of job.')
@click.option('--fields', type=click.STRING,
              default='id,filename,progress,state,data.aggregated_status,name', show_default=True,
              help='Comma separated list of fields that will be in response')
@click.option('--root-only', type=click.BOOL, default=True, show_default=True,
              help='Boolean. Shows root only or all jobs.')
@click.option('--page-size', type=click.INT, default=1000,
              help='Max size of data that will be returned in response.')
@click.option('--offset', type=click.INT,
              help='Begin result set at this index.')
@click.option('--wrap-table', default=True, show_default=True, type=click.BOOL,
              help='Wrap result table to fit with screen.')
@utils.add_host_options
@utils.add_auth_options
@utils.add_credentials_options
@cli.pass_context
@utils.handle_exceptions
@utils.check_cis_version
def list_(ctx, **kwargs):
    split_values = lambda comma_separated_values: list(map(str.strip, map(str, comma_separated_values.split(','))))
    if kwargs.get('job_type') is not None:
        kwargs['job_type'] = split_values(kwargs['job_type'])
    if kwargs.get('path_list_file') is not None and kwargs.get('destination_path') is not None:
        raise exception.OptionException("Please specify only one option --path-list-file or --destination-path")
    if kwargs.get('path_list_file') is not None:
        with open(kwargs['path_list_file']) as f:
            file_content = f.read()
        path = map(str.strip, file_content.strip().split('\n'))
        kwargs['path'] = list(path)
    if kwargs.get('destination_path') is not None:
        kwargs['path'] = split_values(kwargs['destination_path'])
    if kwargs.get('state') is not None:
        kwargs['state'] = split_values(kwargs['state'])
    if kwargs.get('state_simple') is not None:
        kwargs['state_simple'] = split_values(kwargs['state_simple'])
    if kwargs.get('fields') is not None:
        kwargs['fields'] = split_values(kwargs['fields'])
    kwargs['with_children'] = True
    jobs = jobs_client.get_jobs(
        kwargs.pop('north_host'), **kwargs)
    for job_data in jobs['data']:
        for datatime_filed in job_datetime_fields:
            if job_data.get(datatime_filed):
                job_data[datatime_filed] = utils.convert_epoch_to_date(job_data[datatime_filed])
        if 'progress' in job_data:
            try:
                job_data['progress'] = '{} %'.format(int(float(job_data['progress']) * 100))
            except (ValueError, TypeError):
                job_data['progress'] = ''
        if 'children_jobs' in job_data and kwargs.get('path'):
            job_data['subjobs progress'] = ''
            if job_data.get('state_simple') != 'completed':
                # do not show subjobs progress for completed tasks
                for subjob in job_data['children_jobs']:
                    job_data['subjobs progress'] += '"{}" has status "{}"\n'.format(
                        subjob.get('name'), subjob.get('state_simple') or subjob.get('state'))
        if 'data' in job_data and job_data['data'] and 'aggregated_status' in job_data['data']:
            job_data['data.aggregated_status'] = job_data.get('data', {}).get('aggregated_status', '')
        if 'log' in job_data and type(job_data['log']) is list:
            job_data['log'] = '\n'.join(job_data['log'])
    table_fields = kwargs.get('fields')
    if table_fields and kwargs.get('path'):
        table_fields.append('subjobs progress')
    if ('state' in table_fields and
            jobs['data'] and jobs['data'][0].get('state_simple')):  # try to do it independently from CIS version
        table_fields = list(map(lambda field: 'state_simple' if field == 'state' else field, table_fields))
    utils.display("Total count of jobs: {}, offset: {}, page size: {}".format(
        jobs.get('total'), kwargs.get('offset') or 0, kwargs['page_size']))
    printer.print_json_as_table(
        jobs['data'],
        header_field_map={
            'state_simple': 'state', 'data.aggregated_status': 'aggregated status'},
        order_fields=table_fields,
        wrap_text=kwargs['wrap_table'])


@job_cli.command('get', context_settings=utils.CONTEXT_SETTINGS, help='Gets job info.')
@click.option('--job-id', required=True, type=click.STRING, help='Job ID.')
@click.option('--format', type=click.Choice(['full', 'brief']),
              default='full', show_default=True, help='Show all job\'s fields of specific fields only.')
@click.option('--wrap-table', default=True, show_default=True, type=click.BOOL,
              help='Wrap result table to fit with screen.')
@utils.add_host_options
@utils.add_auth_options
@utils.add_credentials_options
@cli.pass_context
@utils.handle_exceptions
@utils.check_cis_version
def get(ctx, **kwargs):
    job_id = kwargs.pop('job_id')
    jobs = jobs_client.get_job(kwargs.pop('north_host'), job_id, **kwargs)
    jobs_dict = collections.OrderedDict()
    for field in ('name', 'filename', 'type', 'state_simple', 'ingest_point'):
        jobs_dict[field] = jobs.pop(field, None)
    jobs_dict.update(jobs)
    for job_key, job_val in jobs_dict.items():
        if type(job_val) is list:
            jobs_dict[job_key] = '\n'.join(map(text, job_val))
        if job_key in job_datetime_fields:
            if jobs_dict.get(job_key):
                jobs_dict[job_key] = utils.convert_epoch_to_date(jobs_dict[job_key])
        if 'progress' == job_key:
            try:
                jobs_dict['progress'] = '{} %'.format(int(float(jobs_dict['progress']) * 100))
            except (ValueError, TypeError):
                jobs_dict['progress'] = ''
    jobs_table = [{'key': key, 'value': value} for key, value in jobs_dict.items()]
    printer.print_json_as_table(
        jobs_table,
        not_print_header=True,
        order_fields=('key', 'value'),
        wrap_text=kwargs['wrap_table']
    )
