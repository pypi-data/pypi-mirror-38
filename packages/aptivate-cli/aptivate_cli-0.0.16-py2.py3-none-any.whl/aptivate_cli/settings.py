"""A configuration settings module."""

from os import environ

ANSIBLE_HOME_DIRECTORY = '.ansible'
ANSIBLE_REQUIREMENTS_FILE = 'requirements.yml'
ANSIBLE_PLAYBOOKS_DIRECTORY = 'playbooks'
ANSIBLE_PLAYBOOK_FILE = 'deploy.yml'

PROJECT_PLAY_REPOSITORY_URL = 'https://git.coop/aptivate/ansible-plays/{}-play'
PROJECT_APP_REPOSITORY_URL = 'https://git.coop/aptivate/{}'

ROLE_TEMPLATE_URL = 'https://git.coop/aptivate/templates/role'
PLAY_TEMPLATE_URL = 'https://git.coop/aptivate/templates/play'

APTIVATE_CLI_MYSQL_PASS = 'APTIVATE_CLI_MYSQL_PASS'
APTIVATE_CLI_SUDO_PASS = 'APTIVATE_CLI_SUDO_PASS'
APTIVATE_CLI_PASS_DIR = 'APTIVATE_CLI_PASS_DIR'
APTIVATE_CLI_SSH_USER = 'APTIVATE_CLI_SSH_USER'

IS_GITLAB_CI = environ.get('GITLAB_CI', False)
