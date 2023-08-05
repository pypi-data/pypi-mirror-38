from __future__ import unicode_literals

from functools import wraps
import sys
import imp
import json
import os
import os.path
import stat
import time
import hashlib
import contextlib
import threading

import requests
import click
from past.builtins import basestring

import cis_client
from cis_client import exception
from cis_client.lib.cis_north import version_client
from cis_client.lib.cis_north import jobs_client

# import progressbar2 here (not progressbar)
correct_progressbar_loaded = False
for path__ in sys.path:
    try:
        imp.load_module('progressbar2', *imp.find_module('progressbar', [path__]))
        import progressbar2
        pb = progressbar2.ProgressBar(max_value=100)
        correct_progressbar_loaded = True
        break
    except (ImportError, TypeError) as e:
        pass
if correct_progressbar_loaded is False:
    print("Please reinstall application. progressbar2 is not installed")
    sys.exit(1)


CONTEXT_SETTINGS = dict(auto_envvar_prefix='CIS_CLIENT')


def add_auth_options(func):
    @click.option('--brand-id', type=click.STRING, help='Brand Id')
    @click.option('--account-id', type=click.STRING, help='Account Id')
    @click.option('--group-id', type=click.STRING, help='Group Id')
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def add_host_options(func):
    @click.option('--aaa-host', required=True, type=click.STRING, help='AAA hostname.')
    @click.option('--north-host', required=True, type=click.STRING, help='CIS North hostname.')
    @click.option('--insecure', type=click.BOOL, default=False, show_default=True, is_flag=True,
                  help='Allow insecure server connections when using SSL')
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def add_credentials_options(func):
    @click.option('--username', required=True, type=click.STRING, help='AAA username.')
    @click.option('--password', required=True, type=click.STRING, help='AAA password.',
                  prompt='Password', hide_input=True)
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@contextlib.contextmanager
def handle_exceptions_contextmanager(reraise=False, exit_on_exception=True):
    try:
        yield
    except requests.HTTPError as e:
        reason = e.response.text
        try:
            jsonified_reason = json.loads(reason)
            reason = jsonified_reason['message']
        except Exception:
            pass
        display("Error: {}".format(reason))
        if exit_on_exception:
            sys.exit(1)
    except (exception.OptionException, exception.UploadConflictException) as e:
        display("Error: {}".format(str(getattr(e, 'message', None) or e)))
        if exit_on_exception:
            sys.exit(1)
    except exception.AsperaExecutableNotFound as e:
        display("Error: {}".format(e.message))
        if exit_on_exception:
            exit(1)
    except exception.HttpClientError as e:
        display("Error: {}".format(e.message))
        if exit_on_exception:
            exit(1)
    except Exception as e:
        # just to ease debug
        import traceback
        trace = traceback.format_exc()
        if reraise is True:
            raise
        else:
            display("Error: {}".format(str(getattr(e, 'message', None) or e)))
            if exit_on_exception:
                sys.exit(1)


def handle_exceptions(func):
    def wrapper(context, *args, **kwargs):
        with handle_exceptions_contextmanager(reraise=context.verbose):
            func(context, *args, **kwargs)
    return wrapper


def get_source_file_list_from_kwargs(**kwargs):
    split_values = lambda comma_separated_values: map(str.strip, map(str, comma_separated_values.split(',')))
    source_file_list = kwargs.get('source_file_list')
    source_file = kwargs.get('source_file')
    if source_file_list is not None and source_file is not None:
        raise exception.OptionException("Please specify only one option --source-file-list or --source-file")
    if not source_file_list and not source_file:
        raise exception.OptionException("Please specify either option --source-file-list or --source-file option")
    paths = []
    if source_file_list is not None:
        with open(source_file_list) as f:
            file_content = f.read()
        paths = [path_item.strip() for path_item in file_content.strip().split('\n')]
    if source_file is not None:
        paths = split_values(source_file)

    valid_paths = []
    for path in paths:
        try:
            stat_info = os.stat(path)
            if stat.S_ISDIR(stat_info.st_mode):
                sub_paths = os.listdir(path)
                for sub_path in sub_paths:
                    full_sub_path = os.path.join(path, sub_path)
                    sub_stat_info = os.stat(full_sub_path)
                    if stat.S_ISDIR(sub_stat_info.st_mode):
                        display('Skip second level directory {}'.format(full_sub_path))
                        continue
                    valid_paths.append(full_sub_path)
            else:
                valid_paths.append(path)
        except Exception as e:
            if kwargs.get('skip_errors') is not True:
                raise
            display("Error: {}".format(str(getattr(e, 'message', None) or e)))

    return valid_paths


def check_cis_version(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        cis_version = version_client.get_cis_version(**kwargs)
        if isinstance(cis_version, basestring):
            if not cis_version.startswith(cis_client.SUPPORTED_CIS_VERSION):
                display(
                    "Backend CIS version {} is not supported by udn-cis-client. Please install a new version of udn-cis-client:\n"\
                    "pip install --upgrade udn-cis-client".format(cis_version))
                sys.exit(1)
        else:  # dict
            from cis_client import cli
            cli_version_tuple = cli.app_version.version.split('.')
            cli_version_major = str(cli_version_tuple[0])
            cli_version_minor = str(cli_version_tuple[1])

            # TODO remove me later...
            # release 3.3 contains not updated cis-client version... so
            cis_api = cis_version['cis-api']
            if cis_api.startswith('3.3'):
                cis_version['cis-client'] = "1.5"

            cis_version_tuple = cis_version['cis-client'].split('.')
            cis_version_major = str(cis_version_tuple[0])
            cis_version_minor = str(cis_version_tuple[1])
            if cli_version_major != cis_version_major or cli_version_minor != cis_version_minor:
                display(
                    "Backend CIS version is not supported by udn-cis-client. Current version of udn-cis-client is {cli_version}.\n"\
                    "To connect to server please install a new version of udn-cis-client:\n"\
                    "pip install udn-cis-client=={cis_version_major}.{cis_version_minor}".format(
                        cli_version=cli.app_version,
                        cis_version_major=cis_version_major,
                        cis_version_minor=cis_version_minor))
                sys.exit(1)
        func(*args, **kwargs)
    return wrapper


class ProgressBar(progressbar2.ProgressBar):
    def __init__(self, *args, **kwargs):
        super(ProgressBar, self).__init__(*args, **kwargs)
        self.exception = None

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.exception = exc_type
        self.finish()

    def update(self, value=None, force=False, **kwargs):
        if self.exception:
            value = 0
        super(ProgressBar, self).update(value, force, **kwargs)


def display(string):
    if sys.version_info < (3, 0):
        print(string.encode('utf-8'))
    else:
        print(string)


def convert_epoch_to_date(epoc):
    format = '%Y-%m-%d %H:%M:%S'
    return time.strftime(format, time.gmtime(epoc))


def humanize_file_size(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    formatted_time = "%.1f%s%s" % (num, 'Yi', suffix)
    return formatted_time


def md5(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    checksum = hash_md5.hexdigest()
    return checksum


class ChecksumCalculator(object):
    def __init__(self):
        self.full_dst_path_2_path = {}
        self._path_2_md5 = {}
        self._thread = threading.Thread(target=self._loop)
        self._thread.daemon = True
        self._wait_for_files = True

    def md5sum(self, path, full_dst_path):
        self.full_dst_path_2_path[full_dst_path] = path
        self._calculate()

    def join(self):
        self._wait_for_files = False
        while self._thread.is_alive():
            self._thread.join(timeout=1)

    def get_md5(self, full_dst_path):
        return self._path_2_md5[self.full_dst_path_2_path[full_dst_path]]

    def _loop(self):
        while True:
            uploaded = self.full_dst_path_2_path.values()
            md5_done = self._path_2_md5.keys()
            md5_todo = set(uploaded) - set(md5_done)
            if self._wait_for_files is False and len(md5_todo) == 0:
                break
            for path in md5_todo:
                self._path_2_md5[path] = md5(path)
            time.sleep(0.1)

    def _calculate(self):
        if not self._thread.is_alive():
            self._thread.start()


def wait_job_done(north_host, path_list, wait_timeout=60*10,  **kwargs):
    end_time = time.time() + wait_timeout
    while True:
        try:
            if time.time() > end_time:
                raise exception.ChecksumJobTimeout()
            jobs = jobs_client.get_jobs(
                north_host, path=path_list, job_type=['checksum-generate'], latest='true', **kwargs)
            failed_checksum_jobs = list(filter(lambda job: job['state_simple'] == 'failed', jobs['data']))
            if failed_checksum_jobs:
                raise exception.ChecksumJobsFailed(list(map(lambda job: job['filename'], failed_checksum_jobs)))
            if len(jobs['data']) == len(path_list):
                simple_statuses = list(map(lambda job: job['state_simple'], jobs['data']))
                if set(simple_statuses) == set(['completed']):
                    display('All checksum jobs were completed.')
                    break
            time.sleep(5)
        except exception.HttpClientError as e:
            import traceback
            x = traceback.format_exc()
            time.sleep(5)


class AuthKeeper(object):

    TOKEN_EXPIRATION_TIME = 50 * 60

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.north_host = kwargs.pop('north_host')
        self.aaa_host = kwargs['aaa_host']
        self.insecure = kwargs['insecure']
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.ingest_point = kwargs.pop('ingest_point')
        self._token = None
        self._access_key = None
        self._token_issued = None
        self._locker = threading.RLock()

    def get_token(self):
        with self._locker:
            if self.is_expired():
                self.refresh_token()
            return self._token

    def get_access_key(self):
        from cis_client.lib.cis_north import access_key_client
        with self._locker:
            if self.is_expired():
                self.refresh_token()
            if not self._access_key:
                access_client = access_key_client.AccessKeyClient(self.north_host, insecure=self.insecure)
                access_key = access_client.create_access_key(self._token, self.ingest_point, **self.kwargs)
                self._access_key = access_key
            return self._access_key

    def refresh_token(self):
        with self._locker:
            self._token = None
            self._access_key = None
            self._token_issued = None
            token_issued = time.time()
            from cis_client.lib.aaa import auth_client
            self._token = auth_client.get_token(
                self.aaa_host, self.username, self.password, insecure=self.insecure)
            self._token_issued = token_issued

    def is_expired(self):
        with self._locker:
            if not self._token or not self._token_issued:
                return True
            if time.time() > self._token_issued + self.TOKEN_EXPIRATION_TIME:
                return True
            return False
