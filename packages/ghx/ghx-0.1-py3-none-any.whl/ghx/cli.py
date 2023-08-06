import logging
import os
import subprocess
import sys
import tempfile
from collections import namedtuple

import click

logger = logging.getLogger(__name__)

command_help = """\
Runs a command from a GitHub repository.

PATH indicates the repository form which code needs to be retrieved,
in "organization/reponame" format.

Optionally, a script path can be added. If omitted, ``bin/run`` will
be assumed.

Examples:

- ``rshk/ghx-example``

- ``rshk/ghx-example/bin/run`` (same as the above)

- ``rshk/ghx-example/bin/two``
"""


class ScriptPathParamType(click.ParamType):

    name = 'script_path'

    def convert(self, value, param, ctx):
        return parse_repo_path(value)


ScriptPath = namedtuple('ScriptPath', 'org,repo,path')


@click.command(context_settings={
    # We want to forward arguments to the called command.
    # Options to ghx *must* come before the path
    'allow_interspersed_args': False,
    'allow_extra_args': True,
}, help=command_help)
@click.option('-b', '--branch', default='master',
              help='Git branch to clone. Defaults to "master".')
@click.option('-v', '--verbose', default=False, is_flag=True)
@click.argument('path', type=ScriptPathParamType())
@click.argument('args', nargs=-1)
def main(branch, path, args, verbose=False):

    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.StreamHandler(sys.stderr))

    logger.debug(f'Repo path: {path}')
    logger.debug(f'Branch: {branch}')
    logger.debug(f'Args: {args}')

    destdir = mkdtemp()
    repo_url = get_github_repo_url(path.org, path.repo)
    shallow_clone(destdir, repo_url, branch=branch, verbose=verbose)

    executable = os.path.join(destdir, path.path)
    command_args = [executable, *args]

    logger.debug(f'Running {command_args}')
    logger.debug('-' * click.get_terminal_size()[0])

    os.execv(executable, command_args)


def parse_repo_path(path):
    parts = path.split('/', 2)
    if len(parts) < 2 or not parts[0] or not parts[1]:
        raise ValueError('Script path must be in org/repo[/path] format')
    return ScriptPath(
        parts[0], parts[1],
        parts[2] if len(parts) > 2 else 'bin/run')


def get_cache_home():
    cache = os.environ.get('XDG_CACHE_HOME')
    if cache:
        return cache
    return os.path.expanduser('~/.cache')


def get_cache_dir():
    return os.path.join(get_cache_home(), 'ghx')


def shallow_clone(destdir, repo, branch='master', verbose=False):
    command = ['git', 'clone', '--depth=1', '--branch', branch, repo, destdir]
    OUTSTREAM = None if verbose else subprocess.DEVNULL
    subprocess.check_call(command, stdout=OUTSTREAM, stderr=OUTSTREAM)


def get_github_repo_url(organization, repo_name):
    return 'https://github.com/{}/{}'.format(organization, repo_name)


def mkdtemp():
    return tempfile.mkdtemp(prefix='ghx-')
