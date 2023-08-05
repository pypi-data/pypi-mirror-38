"""Command line entry point."""

import click

from aptivate_cli.cligroups.ci.commands import (
    checks, isort, pylava, pytest, link
)
from aptivate_cli.cligroups.deploy.commands import deploy
from aptivate_cli.cligroups.remotes.commands import load, login, shell
from aptivate_cli.cligroups.templates.commands import template
from aptivate_cli.config import Config, pass_config


@click.group()
@click.version_option()
@pass_config
def main(config: Config) -> None:
    """
    \b
      __ _ _ __ | |_(_)_   ____ _| |_ ___        ___| (_)
     / _` | '_ \| __| \ \ / / _` | __/ _ \_____ / __| | |
    | (_| | |_) | |_| |\ V / (_| | ||  __/_____| (__| | |
     \__,_| .__/ \__|_| \_/ \__,_|\__\___|      \___|_|_|
          |_|
    """  # noqa


main.add_command(deploy)
main.add_command(template)
main.add_command(checks)
main.add_command(pylava)
main.add_command(isort)
main.add_command(pytest)
main.add_command(link)
main.add_command(login)
main.add_command(shell)
main.add_command(load)
