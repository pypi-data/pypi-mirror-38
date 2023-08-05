"""A module for shell commands."""

import shlex
from subprocess import CalledProcessError, call
from os import getcwd
from os.path import abspath, basename, exists
from typing import Any, Dict

import click

from aptivate_cli.config import Config
from aptivate_cli.settings import (
    APTIVATE_CLI_MYSQL_PASS,
    APTIVATE_CLI_SUDO_PASS,
    APTIVATE_CLI_SSH_USER,
)


def cli_run(command: str,
            cwd: str = None,
            env: Dict[str, str] = None,
            shell: bool = False,
            ) -> Any:
    """A handler for command running with nice colours.

    Within reason, this function should handle all subprocess calls to external
    programs in a uniform way to keep the rest of library logic simple.
    """
    explained = (
        'cd {} && {}'.format(basename(cwd), command)
        if cwd is not None else command
    )
    click.secho(explained, fg='green')

    command_kwargs: Dict[str, Any] = {}
    if env:
        command_kwargs['env'] = env
    if cwd:
        command_kwargs['cwd'] = cwd
    if shell:
        command_kwargs['shell'] = shell

    formatted_cmd = command if shell else shlex.split(command)
    return_code = call(formatted_cmd, **command_kwargs)

    if return_code != 0:
        raise CalledProcessError(returncode=return_code, cmd=command)

    return return_code


def clone_template(template, no_input=False) -> None:
    """Clone a cookiecutter template."""
    command = (
        'cookiecutter -f --no-input {}'
        if no_input else 'cookiecutter -f {}'
    )
    try:
        cli_run(command.format(template))
    except CalledProcessError as exception:
        message = str(exception)
        raise click.ClickException(click.style(message, fg='red'))


def create_ansible_home(config) -> None:
    """Create the Ansible home directory."""
    if not exists(config.ansible_home_path):
        try:
            cli_run('mkdir {}'.format(basename(config.ansible_home_path)))
        except CalledProcessError as exception:
            message = str(exception)
            raise click.ClickException(click.style(message, fg='red'))


def git_clone_project_play(config: Config) -> None:
    """Clone the project play."""
    if not exists(config.project_play_path):
        command = 'git clone {}'.format(config.project_play_url)
        try:
            cli_run(command, cwd=config.ansible_home_path)
        except CalledProcessError as exception:
            message = str(exception)
            raise click.ClickException(click.style(message, fg='red'))


def pipenv_sync_project_play(config: Config) -> None:
    """Run a Pipenv sync on the project."""
    try:
        cli_run('pipenv sync', cwd=config.project_play_path)
    except CalledProcessError as exception:
        message = str(exception)
        raise click.ClickException(click.style(message, fg='red'))


def galaxy_install_project_play(config: Config) -> None:
    """Run an ansible-galaxy requirements install."""
    command = 'pipenv run ansible-galaxy install -r {}'.format(
        config.galaxy_requirements_file
    )
    try:
        cli_run(command, cwd=config.project_play_path)
    except CalledProcessError as exception:
        message = str(exception)
        raise click.ClickException(click.style(message, fg='red'))


def pipenv_run_ansible_play(config: Config, env: str) -> None:
    """Run the project playbook based on the environment."""
    playbook = config.playbook_path(env)

    extra_vars = {}
    if env == 'dev':
        config.prompt_for_secret_values(['sudo_pass', 'mysql_pass'])
        extra_vars.update({
            'django_dev_project_root': abspath(getcwd()),
            'django_dev_project_name': config.project_name,
            'ansible_become_pass': config.env_vars[APTIVATE_CLI_SUDO_PASS],
            'mysql_root_password': config.env_vars[APTIVATE_CLI_MYSQL_PASS],
        })
    else:
        config.env_var_checks()

    command = 'pipenv run ansible-playbook {}'.format(playbook)

    if extra_vars:
        joined = ' '.join('{}={}'.format(k, v) for k, v in extra_vars.items())
        command = '{} --extra-vars "{}"'.format(command, joined)

    try:
        cli_run(command, cwd=config.project_play_path)
    except CalledProcessError as exception:
        message = str(exception)
        raise click.ClickException(click.style(message, fg='red'))


def remote_login(config: Config, env: str) -> None:
    """SSH into a remote server."""
    machine = config.remote_machine(env)
    config.prompt_for_values(['ssh_user'])
    command = 'ssh {}@{}'.format(
        config.env_vars[APTIVATE_CLI_SSH_USER],
        machine,
    )
    try:
        cli_run(command)
    except CalledProcessError as exception:
        message = str(exception)
        raise click.ClickException(click.style(message, fg='red'))


def remote_shell(config: Config, env: str) -> None:
    """Run a remote django shell."""
    machine = config.remote_machine(env)
    config.prompt_for_values(['ssh_user'])
    shell_command = 'pipenv run python manage.py shell'
    command = (
        "ssh -t {}@{} 'cd {} && {}'".format(
            config.env_vars[APTIVATE_CLI_SSH_USER],
            machine,
            config.remote_project_path,
            shell_command
        )
    )
    try:
        cli_run(command)
    except CalledProcessError as exception:
        message = str(exception)
        raise click.ClickException(click.style(message, fg='red'))


def remote_load(config: Config, env: str) -> None:
    """Retrieve a MySQL dump from a remote machine."""
    machine = config.remote_machine(env)

    config.prompt_for_values(['ssh_user'])
    ssh_user = config.env_vars[APTIVATE_CLI_SSH_USER]

    config.prompt_for_secret_values(['mysql_pass'])
    mysql_pass = config.env_vars[APTIVATE_CLI_MYSQL_PASS]

    ssh_connect = 'ssh {}@{}'.format(ssh_user, machine)
    scp_connect = 'scp {}@{}'.format(ssh_user, machine)
    dump_path = '/tmp/{}-dump.sql'.format(config.project_name)

    dump_cmd = "{ssh} 'sudo mysqldump {db} > {path}'"

    try:
        cli_run(dump_cmd.format(
            ssh=ssh_connect,
            db=config.project_name,
            path=dump_path
        ))
    except CalledProcessError as exception:
        message = str(exception)
        raise click.ClickException(click.style(message, fg='red'))

    scp_cmd = '{scp}:{remote_path} {local_path}'

    try:
        cli_run(scp_cmd.format(
            scp=scp_connect,
            remote_path=dump_path,
            local_path=dump_path,
        ))
    except CalledProcessError as exception:
        message = str(exception)
        raise click.ClickException(click.style(message, fg='red'))

    load_cmd = 'mysql -uroot -p{pword} {db} < {sql}'

    try:
        cli_run(load_cmd.format(
            pword=mysql_pass,
            db=config.project_name,
            sql=dump_path
            ), shell=True
        )
    except CalledProcessError as exception:
        message = str(exception)
        raise click.ClickException(click.style(message, fg='red'))


def django_checks(config: Config) -> None:
    """Run Django application checks."""
    config.django_checks()

    commands = [
        'pipenv run python manage.py check',
        'pipenv run python manage.py makemigrations --check',
    ]

    for command in commands:
        try:
            cli_run(command)
        except CalledProcessError as exception:
            message = str(exception)
            raise click.ClickException(click.style(message, fg='red'))


def pylava_checks(config: Config, arguments: str) -> None:
    """Run pylava checks."""
    config.django_checks()

    try:
        cli_run('pipenv run pylava {}'.format(arguments))
    except CalledProcessError as exception:
        message = str(exception)
        raise click.ClickException(click.style(message, fg='red'))


def isort_checks(config: Config, arguments: str) -> None:
    config.django_checks()

    try:
        cli_run('pipenv run isort {}'.format(arguments))
    except CalledProcessError as exception:
        message = str(exception)
        raise click.ClickException(click.style(message, fg='red'))


def pytest_runner(config: Config, arguments: str) -> None:
    """Run pytest."""
    config.django_checks()

    try:
        cli_run('pipenv run pytest {}'.format(arguments))
    except CalledProcessError as exception:
        message = str(exception)
        raise click.ClickException(click.style(message, fg='red'))


def link_settings(config: Config, env: str) -> None:
    """Link Django application settings."""
    config.django_checks()

    try:
        cwd = '{}/{}'.format(abspath(getcwd()), config.project_name)
        src = '{}/local_settings.py.{}'.format(cwd, env)
        dst = '{}/local_settings.py'.format(cwd)
        cli_run('ln -srf {} {}'.format(src, dst))
    except CalledProcessError as exception:
        message = str(exception)
        raise click.ClickException(click.style(message, fg='red'))
