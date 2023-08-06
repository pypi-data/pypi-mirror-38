from subprocess import check_output

import click
from IPython.terminal.embed import InteractiveShellEmbed

ipshell = InteractiveShellEmbed()
ipshell.dummy_mode = True


def get_version():
    import shell_timeit

    return shell_timeit.__version__


@click.command()
@click.argument("cmd", nargs=-1)
@click.version_option(version=get_version())
def entry(cmd):
    if len(cmd) == 0:
        raise click.BadParameter("Empty string.", param_hint="cmd")
    cmd = " ".join(cmd)

    def run_cmd():
        check_output(cmd, shell=True)

    click.echo("Estimating running time...")
    ipshell.magic("timeit run_cmd()")
