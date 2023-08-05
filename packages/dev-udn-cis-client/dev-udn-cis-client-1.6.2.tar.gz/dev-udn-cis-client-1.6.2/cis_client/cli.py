import os
import sys
import pkg_resources
import click
click.disable_unicode_literals_warning = True

from cis_client.commands import utils


app_version = pkg_resources.working_set.by_key['dev-udn-cis-client']


class Context(object):

    def __init__(self):
        self.verbose = False

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)


pass_context = click.make_pass_decorator(Context, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          'commands'))


class CisClientCLI(click.MultiCommand):
    def load_commands(self):
        from cis_client.commands import cmd_job
        from cis_client.commands import cmd_upload
        from cis_client.commands import cmd_workflow
        from cis_client.commands import cmd_profile
        from cis_client.commands import cmd_ingest_point
        from cis_client.commands import cmd_cluster
        from cis_client.commands import cmd_content

        self.commands = {
            'upload': cmd_upload.cli,
            'job': cmd_job.job_cli,
            'workflow': cmd_workflow.workflow_cli,
            'profile': cmd_profile.profile_cli,
            'ingest-point': cmd_ingest_point.ingest_point_cli,
            'cluster': cmd_cluster.cluster_cli,
            'content': cmd_content.content_cli,
        }

    def list_commands(self, ctx):
        self.load_commands()
        rv = list(self.commands.keys())
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        self.load_commands()
        return self.commands.get(name)


@click.command(cls=CisClientCLI, context_settings=utils.CONTEXT_SETTINGS)
@click.option('-v', '--verbose', is_flag=True,
              help='Enables verbose mode.')
@click.version_option(version=app_version.version)
@pass_context
def cli(ctx, verbose):
    ctx.verbose = verbose
