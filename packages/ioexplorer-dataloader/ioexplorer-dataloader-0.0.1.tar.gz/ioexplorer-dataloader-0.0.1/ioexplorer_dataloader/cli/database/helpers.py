import os
import json
import pkg_resources
import subprocess as sp
from textwrap import dedent
from PyInquirer import prompt
from ..common.decorators import read_conf
from ..common.logging import error, success, info

def check_docker_installed():
    try:
        sp.check_call(['docker'], stdout=sp.PIPE, stderr=sp.PIPE)
    except (FileNotFoundError, sp.CalledProcessError) as e:
        print(e)
        error(dedent(
            '''\
            Docker could not be used (is it installed?)
            I need Docker to create a database.

            Install Docker here: https://docs.docker.com/install/
            '''))


create_database_questions = [
    {
        'type': 'input',
        'name': 'database',
        'message': 'Name the database',
        'default': 'default'
    },
    {
        'type': 'input',
        'name': 'host',
        'message': 'Choose a host.',
        'default': '127.0.0.1'
    },
    {
        'type': 'input',
        'name': 'port',
        'message': 'Choose a port.',
        'default': '5432'
    },
    {
        'type': 'input',
        'name': 'username',
        'message': 'Choose a username for the root account.',
        'default': 'root'
    },
    {
        'type': 'password',
        'name': 'password',
        'message': 'Choose a password for the root account.'
    }
]

def create_database(conf_folder):
    check_docker_installed()
    if conf_folder is None:
        conf_folder = 'ioexplorer_database_configs'
        if os.path.exists(conf_folder):
            error(dedent("""\
            You did not set the `--database-config` flag or the
            `IOEXPLORER_DATABASE_CONFIG` environment variable,
             but there is a `{}` folder in this directory.

             Please set that correctly!!""".format(conf_folder)))

        os.mkdir(conf_folder)

        info("You did not include a path to a database config folder, so I am creating one in this directory. "
             "Look for a folder called `{}`.".format(conf_folder))

    ans = prompt(create_database_questions)
    ans['dialect'] = 'postgres'
    name = ans['database']
    conf_path = os.path.join(conf_folder, '{}.config.json'.format(name))
    if os.path.exists(conf_path):
        error("There is already a database config file for '{}' in the database config folder at `{}`"
              .format(name, conf_folder))
    with open(conf_path, 'w') as f:
        json.dump(ans, f)
    success('Created the database configuration for {}'.format(name))


@read_conf
def start_database(database_name, conf):
    check_docker_installed()
    try:
        sp.check_call([
            'docker',
            'run',
            '-p', '{:d}:5432'.format(int(conf['port'])),
            '--name', database_name,
            '-e', 'POSTGRES_USER={}'.format(conf['username']),
            '-e', 'POSTGRES_PASSWORD={}'.format(conf['password']),
            '-e', 'POSTGRES_DB={}'.format(database_name),
            '-d',
            'postgres'
        ])
    except sp.CalledProcessError:
        error(dedent(
            '''\
            I could not start the database for some reason :(
            
            Check above for logs from the Docker daemon.
            '''
        ))
    success('Started the database {}'.format(database_name))

@read_conf
def kill_database(database_name, conf):
    check_docker_installed()
    try:
        sp.check_call([
            'docker',
            'rm',
            '-f',
            database_name
        ])
    except sp.CalledProcessError:
        error(dedent(
            '''\
            I could not kill the database for some reason :(
            
            Check above for logs from the Docker daemon.
            '''
        ))
    success('Killed the database {}'.format(database_name))


def migrate_database(database_name, conf):
    conf_path = os.path.join(conf, '{}.config.json'.format(database_name))
    migrations_path = pkg_resources.resource_filename(
        'ioexplorer_dataloader',
        'ioexplorer-database-migrations'
    )
    try:
        sp.check_call([
            'sequelize',
            'db:migrate',
            '--config', conf_path,
            '--migrations-path', migrations_path
        ])
    except (FileNotFoundError, sp.CalledProcessError):
        error(dedent(
            '''\
            I could not migrate the database. Is `sequelize-cli` installed?
            '''
        ))

@read_conf
def shell_database(database_name, conf):
    check_docker_installed()
    try:
        sp.check_call([
            'docker',
            'exec',
            '-it',
            '-e', 'POSTGRES_USER={}'.format(conf['username']),
            '-e', 'POSTGRES_PASSWORD={}'.format(conf['password']),
            database_name,
            'psql',
            '-d',
            database_name

        ])
    except sp.CalledProcessError:
        error(dedent(
            '''\
            I could not shell into the database. Is `docker` installed?
            '''
        ))
