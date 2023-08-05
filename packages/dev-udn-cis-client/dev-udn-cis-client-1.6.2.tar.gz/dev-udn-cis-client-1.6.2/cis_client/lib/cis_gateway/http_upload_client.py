import os.path
import json
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import pycurl

from cis_client import exception


class ContentClient(object):
    api_version = 'v1'

    def __init__(self, hostname, port, schema='http', insecure=False):
        super(ContentClient, self).__init__()
        self.schema = schema
        self.hostname = hostname
        self.port = port
        self.insecure = insecure

    def get_endpoint(self, dest_path):
        endpoint = "{schema}://{hostname}:{port}/{api_version}/{dest_path}".format(
            schema=self.schema,
            hostname=self.hostname,
            port=self.port,
            api_version=self.api_version,
            dest_path=dest_path)
        return endpoint

    def upload(self, access_key, path, dest_path, overwrite, progress_callback=None):
        stat_info = os.stat(path)

        with open(path, 'rb') as upload_file:
            url = self.get_endpoint(dest_path)
            status_code, reply_body = _pycurl_upload(
                url, progress_callback, stat_info.st_size, upload_file, overwrite, access_key)

            if 400 <= status_code < 600:
                http_error_msg_tmpl = '{reason}. Request {method}: "{url}".'
                reason = ''
                try:
                    jsonified_reason = json.loads(reply_body)
                    reason = jsonified_reason['message']
                except Exception:
                    pass
                method = 'PUT' if overwrite else 'POST'
                if status_code < 500 and not reason:
                    reason = 'Client Error: {}'.format(status_code)
                elif not reason:
                    reason = 'Server Error: {}'.format(status_code)
                http_error_msg = http_error_msg_tmpl.format(reason=reason, method=method, url=url)
                raise exception.HttpClientError(None, 'Uploading was failed.', http_error_msg)

            return reply_body


def _pycurl_upload(url, progress_callback, file_size, upload_file, overwrite, access_key):
    def progress_cb(download_t, download_d, upload_t, upload_d):
        if progress_callback:
            progress_callback(upload_d if upload_d < file_size else file_size)

    response_buffer = StringIO()
    curl = pycurl.Curl()
    curl.setopt(curl.URL, url)
    curl.setopt(pycurl.READFUNCTION, upload_file.read)
    curl.setopt(curl.NOPROGRESS, False)
    curl.setopt(curl.XFERINFOFUNCTION, progress_cb)
    curl.setopt(curl.WRITEDATA, response_buffer)
    curl.setopt(pycurl.PUT if overwrite else pycurl.POST, True)
    curl.setopt(pycurl.HTTPHEADER, [
        'X-Auth-Token: {}'.format(access_key),
        'Content-Type: video/mp4',
        'Content-Length: {}'.format(file_size),
    ])

    # uncomment to DEBUG
    # def header(buf):
    #     import sys
    #     sys.stderr.write(buf)
    # curl.setopt(pycurl.HEADERFUNCTION, header)
    # curl.setopt(pycurl.VERBOSE, 1)

    curl.perform()
    status_code = curl.getinfo(pycurl.HTTP_CODE)
    reply_body = response_buffer.getvalue()
    return status_code, reply_body


def http_upload(ingest_point_info, access_key, path, destination_path=None, overwrite=False,
                progress_callback=None, **kwargs):
    """HTTP upload"""

    if destination_path is None:
        destination_path = os.path.basename(path)

    gateway_hostname = ingest_point_info['gateway']['hostname']
    gateway_port = ingest_point_info['gateway']['protocols']['http']['port']
    content_client = ContentClient(gateway_hostname, gateway_port, insecure=kwargs['insecure'])
    return content_client.upload(access_key, path, destination_path, overwrite, progress_callback)
