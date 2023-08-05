"""Gitlab CI commands module."""

import click

from aptivate_cli.config import Config, pass_config
from aptivate_cli import cmd


@click.command()
@pass_config
def checks(config: Config) -> None:
    """Django checks framework.

    See https://docs.djangoproject.com/en/2.1/ref/checks/.
    """
    cmd.django_checks(config)


@click.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument('pylava_args', nargs=-1, type=click.UNPROCESSED)
@pass_config
def pylava(config: Config, pylava_args: str) -> None:
    """Pylava code audit.

    See https://pylavadocs.readthedocs.io/en/latest/.

    Passes default arguments for convenience:

      * -o=setup.cfg

    Accepts arguments as you might expect:

    $ apc pylava --async --verbose

    Passing arguments overrides the defaults.
    """
    defaults = '-o setup.cfg'
    arguments = ' '.join(pylava_args) if pylava_args else defaults
    cmd.pylava_checks(config, arguments)


@click.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument('isort_args', nargs=-1, type=click.UNPROCESSED)
@pass_config
def isort(config: Config, isort_args: str) -> None:
    """Isort code audit.

    See https://isort.readthedocs.io/.

    Passes default arguments for covenience:

      * -q -rc -c -df -sp setup.cfg

    Accepts arguments as you might expect:

    $ apc isort -rc -y -sp setup.cfg

    Passing arguments overrides the defaults.
    """
    defaults = '-q -rc -c -df -sp setup.cfg'
    arguments = ' '.join(isort_args) if isort_args else defaults
    cmd.isort_checks(config, arguments)


@click.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument('pytest_args', nargs=-1, type=click.UNPROCESSED)
@pass_config
def pytest(config: Config, pytest_args) -> None:
    """Pytest runner.

    Passes default arguments for covenience:

      * -v

    Accepts arguments as you might expect:

    $ apc pytest --cov

    Passing arguments overrides the defaults.
    """
    arguments = ' '.join(pytest_args) if pytest_args else '-v'
    cmd.pytest_runner(config, arguments)


@click.command()
@click.option(
    '--env', '-e',
    type=click.Choice((
        'dev',
        'gitlab',
        'stage',
        'prod'
    )),
    help='The target environment',
    required=True,
    default='dev',
    show_default=True,
)
@pass_config
def link(config: Config, env: str) -> None:
    """Django settings linker."""
    cmd.link_settings(config, env)
