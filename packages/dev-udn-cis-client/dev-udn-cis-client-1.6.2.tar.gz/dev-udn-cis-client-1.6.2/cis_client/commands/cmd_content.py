from __future__ import unicode_literals

import collections
import copy

import click

from cis_client import cli
from cis_client.commands import utils
from cis_client.lib.cis_north import content_client
from cis_client.commands import printer


@click.group(help='Content management.')
def content_cli():
    pass


@content_cli.command('get', context_settings=utils.CONTEXT_SETTINGS, help='Gets content.')
@click.option('--destination-path', type=click.STRING, default='', show_default=True, help='Ingest point path.')
@click.option('--ingest-point', required=True, type=click.STRING, help='Ingest point ID.')
@click.option('--aggregated-status', type=click.STRING,
              help='Filter by aggregated status. Can contain values: "uploading", "processing", "local_done", '
                   '"global_done", "failed".')
@click.option('--filename', type=click.STRING,
              help="Part of a filename. For example if this field is 'cat' following result can match "
                   "'black cat.mp4', 'cat of my neighbor.mp4', etc..")
@click.option('--filter-case-sensitive', type=click.BOOL, default=True, show_default=True,
              help='If true search by filename is case sensitive.')
@click.option('--wrap-table', type=click.BOOL, default=True, show_default=True,
              help='Wrap result table to fit with screen.')
@click.option('--page-size', type=click.INT, default=50, show_default=True,
              help='Max size of data that will be returned in response.')
@click.option('--offset', type=click.INT,
              help='Begin result set at this index.')
@click.option('--sort-by', type=click.STRING, default='name', show_default=True,
              help='Order by column.')
@click.option('--sort-order', type=click.Choice(['asc', 'desc']), default='asc', show_default=True,
              help='Sort order.')
@click.option('--checksum', type=click.Choice(['no', 'md5', 'all']), default='no', show_default=True,
              help='Generate checksum.')
@utils.add_host_options
@utils.add_auth_options
@utils.add_credentials_options
@cli.pass_context
@utils.handle_exceptions
@utils.check_cis_version
def get(ctx, **kwargs):
    ingest_point = kwargs.pop('ingest_point')
    path = kwargs.pop('destination_path')
    content = content_client.get_content(kwargs.pop('north_host'), ingest_point, path, **kwargs)
    utils.display('{} "{}":'.format(content['stat']['type'].capitalize(), path or '/'))

    main_record = prepare_content_record(content)
    if not main_record['name']:
        main_record['name'] = path or '/'
    header_field_map = collections.OrderedDict((
        ('name', 'Name'),
        ('type', 'Type'),
        ('mtime', 'Modification time'),
        ('size', 'Size'),
        ('workflow_id', 'Workflow'),
        ('profile_ids', 'Profile IDs'),
        ('aggregated_status', 'Aggregated status'),
        ('progress', 'Progress'))
    )
    if kwargs.get('checksum') != 'no':
        header_field_map['checksum'] = 'Checksum'
    parent_header_field_map = copy.deepcopy(header_field_map)
    if not main_record['aggregated_status']:
        parent_header_field_map.pop('aggregated_status', None)
    if not main_record['progress']:
        parent_header_field_map.pop('progress', None)
    if not main_record['checksum']:
        parent_header_field_map.pop('checksum', None)
    printer.print_json_as_table(
        [main_record],
        header_field_map=parent_header_field_map,
        order_fields=list(parent_header_field_map.keys()),
        wrap_text=kwargs['wrap_table'],
    )
    if content['stat']['type'] == 'file':
        return
    utils.display('contains {} items'.format(content['total_items']))
    if len(content['items']) == 0:
        return
    utils.display('page size = {}; offset = {}'.format(content['page_size'], content['offset']))

    child_header_field_map = copy.deepcopy(header_field_map)
    records = [prepare_content_record(item) for item in content['items']]
    printer.print_json_as_table(
        records,
        header_field_map=child_header_field_map,
        order_fields=list(child_header_field_map.keys()),
        inner_row_border=False,
        wrap_text=kwargs['wrap_table'],
    )


def prepare_content_record(item):
    record = {
        'name': item.get('name'),
        'atime': utils.convert_epoch_to_date(item['stat']['atime']),
        'mtime': utils.convert_epoch_to_date(item['stat']['mtime']),
        'size': utils.humanize_file_size(item['stat']['size']),
        'type': item['stat']['type'],
        'aggregated_status': (item.get('job') or {}).get('aggregated_status'),
        'progress': (item.get('job') or {}).get('progress'),
        'workflow_id': (item.get('workflow') or {}).get('id') or '',
        'profile_ids': ', '.join((item.get('workflow') or {}).get('profile_ids') or []),
        'checksum': item.get('checksum'),
    }
    if record['progress']:
        record['progress'] = float(record['progress']) * 100
    if record['checksum'] and len(record['checksum']) == 1:
        record['checksum'] = list(record['checksum'].values())[0]
    return record


@content_cli.command('add', context_settings=utils.CONTEXT_SETTINGS, help='Create directory.')
@click.option('--destination-path', type=click.STRING, default='', show_default=True, help='Ingest point path.')
@click.option('--ingest-point', required=True, type=click.STRING, help='Ingest point ID.')
@click.option('--workflow-id', type=click.STRING, help='Workflow ID. For example "abr" or "ism_only".')
@click.option('--profile-ids', type=click.STRING, help='Comma separated list of profile IDs.')
@utils.add_host_options
@utils.add_auth_options
@utils.add_credentials_options
@cli.pass_context
@utils.handle_exceptions
@utils.check_cis_version
def add(ctx, **kwargs):
    split_values = lambda comma_separated_values: list(map(str.strip, map(str, comma_separated_values.split(','))))
    if kwargs.get('profile_ids'):
        kwargs['profile_ids'] = split_values(kwargs['profile_ids'])
    ingest_point = kwargs.pop('ingest_point')
    path = kwargs.pop('destination_path')
    content = content_client.create_directory(kwargs.pop('north_host'), ingest_point, path, **kwargs)
    utils.display('Directory {} was successfully created.'.format(path))


@content_cli.command('modify', context_settings=utils.CONTEXT_SETTINGS, help='Modify directory.')
@click.option('--destination-path', type=click.STRING, default='', show_default=True, help='Ingest point path.')
@click.option('--ingest-point', required=True, type=click.STRING, help='Ingest point ID.')
@click.option('--workflow-id', required=True, type=click.STRING,
              help='Workflow ID. For example "abr" or "ism_only".')
@click.option('--profile-ids', required=True, type=click.STRING, help='Comma separated list of profile IDs.')
@utils.add_host_options
@utils.add_auth_options
@utils.add_credentials_options
@cli.pass_context
@utils.handle_exceptions
@utils.check_cis_version
def modify(ctx, **kwargs):
    split_values = lambda comma_separated_values: list(map(str.strip, map(str, comma_separated_values.split(','))))
    if kwargs.get('profile_ids'):
        kwargs['profile_ids'] = split_values(kwargs['profile_ids'])
    ingest_point = kwargs.pop('ingest_point')
    path = kwargs.pop('destination_path')
    content_client.modify_directory(kwargs.pop('north_host'), ingest_point, path, **kwargs)
    utils.display('Directory "{}" was successfully modified.'.format(path))


@content_cli.command('remove', context_settings=utils.CONTEXT_SETTINGS, help='Remove file or directory.')
@click.option('--destination-path', type=click.STRING, default='', show_default=True, help='Ingest point path.')
@click.option('--ingest-point', required=True, type=click.STRING, help='Ingest point ID.')
@click.option('--recursive', type=click.BOOL, default=False, show_default=True, is_flag=True,
              help='Remove directories and their contents recursively.')
@utils.add_host_options
@utils.add_auth_options
@utils.add_credentials_options
@cli.pass_context
@utils.handle_exceptions
@utils.check_cis_version
def remove(ctx, **kwargs):
    ingest_point = kwargs.pop('ingest_point')
    path = kwargs.pop('destination_path')
    content = content_client.remove(kwargs.pop('north_host'), ingest_point, path, **kwargs)
    utils.display('"{}" was successfully removed.'.format(path))
