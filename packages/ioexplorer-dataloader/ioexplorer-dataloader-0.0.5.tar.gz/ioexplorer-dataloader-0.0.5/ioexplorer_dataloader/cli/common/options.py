import os
import click

def database_config_option(func):
    return click.option(
        '--database-config',
        help='Path to the database config file. '
                'Alternatively, set `IOEXPLORER_DATABASE_CONFIG` environment variable.',
        default=lambda: os.environ.get('IOEXPLORER_DATABASE_CONFIG', None),
        required=True
    )(func)


def database_name_option(func):
    return click.option(
        '--database-name',
        help='Name of the database to load into. '
                'Alternatively, set `IOEXPLORER_DATABASE_NAME` environment variable.',
        default=lambda: os.environ.get('IOEXPLORER_DATABASE_NAME', None),
        required=True
    )(func)