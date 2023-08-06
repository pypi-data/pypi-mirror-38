import os
import click

from .helpers import (
    start_database,
    kill_database,
    shell_database,
    migrate_database
)
from ..common.arguments import database_name_argument
from ..common.decorators import add_env_variables
from ..common.logging import error
from ..common.options import database_config_option

@click.group()
def database():
    pass


@database.command(help='Start the database with name NAME.')
@add_env_variables
def start(_env):
    start_database(
        database_name=_env['database_name'],
        database_port=_env['database_port'],
        database_username=_env['database_username'],
        database_password=_env['database_password']
    )


@database.command(help='Kill the database.')
@add_env_variables
@click.confirmation_option(prompt=click.style("Are you sure you want to delete the database?", fg='red'),
                           help='Confirm the deletion (will not confirm before deletion if set!)')
def kill(_env):
    kill_database(database_name=_env['database_name'])


@database.command(help='Migrate the NAME database')
@add_env_variables
def migrate(_env):
    migrate_database(
        database_name=_env['database_name'],
        database_host=_env['database_host'],
        database_port=_env['database_port'],
        database_username=_env['database_username'],
        database_password=_env['database_password'],
    )
    

@database.command(help='Open a psql shell for the NAME database')
@add_env_variables
def shell(_env):
    shell_database(_env['database_name'],
                   _env['database_username'],
                   _env['database_password'])
