import os
import os.path
import subprocess
import shlex
import errno

from cis_client import exception


def shell_quote(s):
    return "'" + s.replace("'", "'\\''") + "'"


def aspera_upload(ingest_point_info, access_key, path, destination_path=None, max_transfer_rate='1G', **kwargs):
    """Aspera upload"""

    if destination_path is None:
        destination_path = os.path.basename(path)
    destination_path = destination_path.lstrip('/')

    # ASPERA_SCP_PASS=<access-key> ascp -k2 -l1G -P 33001 --user=<username> --host=b.aspera.cdx-dev.dataingest.net
    #  --mode=send file.mp4 <path>
    # aspera_template = ingest_point_info['gateway']['protocols']['aspera']['template']
    hostname = ingest_point_info['gateway']['protocols']['aspera']['hostname']
    aspera_cmd = ' '.join([
        'ascp', '-k2', '-l{}'.format(max_transfer_rate), '-P', '33001',
        '--user', kwargs['username'], '--host', hostname, '--mode=send',
        shell_quote(path), shell_quote(destination_path)])
    aspera_cmd_args = shlex.split(aspera_cmd)
    pipe = subprocess.PIPE if kwargs.get('separate_output') else None
    try:
        process = subprocess.Popen(
            aspera_cmd_args, stdout=pipe, stderr=pipe,
            env=dict(os.environ, **{'ASPERA_SCP_PASS': access_key}))
        process.wait()
        if int(process.returncode) != 0 and kwargs.get('separate_output'):
            stdoutdata, stderrdata = process.communicate()
            from cis_client.commands import utils
            if stdoutdata:
                utils.display(stdoutdata)
            if stderrdata:
                utils.display(stderrdata)
    except OSError as e:
        if e.errno == errno.ENOENT:
            raise exception.AsperaExecutableNotFound()
        raise
    if int(process.returncode) != 0:
        raise exception.AsperaUploadFailed(process.returncode)
