import click

from .helpers import (
    create_database,
    start_database,
    kill_database,
    shell_database,
    migrate_database
)
from ..common.arguments import database_name_argument
from ..common.options import database_config_option

@click.group()
def database():
    pass

@database.command(help='Create a local Postgres database.')
@database_config_option
def create(database_config):
    create_database(database_config)


@database.command(help='Start the database with name NAME.')
@database_name_argument
@database_config_option
def start(name, database_config):
    start_database(name, database_config)


@database.command(help='Kill the database with name NAME.')
@database_name_argument
@database_config_option
@click.confirmation_option(prompt=click.style("Are you sure you want to delete the database?", fg='red'),
                           help='Confirm the deletion (will not confirm before deletion if set!)')
def kill(name, database_config):
    kill_database(name, database_config)


@database.command(help='Migrate the NAME database')
@database_name_argument
@database_config_option
def migrate(name, database_config):
    migrate_database(database_name=name, conf=database_config)
    

@database.command(help='Open a psql shell for the NAME database')
@database_name_argument
@database_config_option
def shell(name, database_config):
    shell_database(name, database_config)
