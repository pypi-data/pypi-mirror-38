"""Remote machine commands module."""

import click

from aptivate_cli.config import Config, pass_config
from aptivate_cli import cmd


@click.option(
    '--env', '-e',
    type=click.Choice(('stage', 'prod')),
    help='The remote machine',
    required=True,
)
@click.command()
@pass_config
def login(config: Config, env: str) -> None:
    """Log into a remote machine."""
    cmd.remote_login(config, env)


@click.option(
    '--env', '-e',
    type=click.Choice(('stage', 'prod')),
    help='The remote machine',
    required=True,
)
@click.command()
@pass_config
def shell(config: Config, env: str) -> None:
    """Django shell on a remote machine."""
    cmd.remote_shell(config, env)


@click.option(
    '--env', '-e',
    type=click.Choice(('stage', 'prod')),
    help='The remote machine',
    required=True,
)
@click.command()
@pass_config
def load(config: Config, env: str) -> None:
    """Retrieve a MySQL dump from a remote machine."""
    cmd.remote_load(config, env)
