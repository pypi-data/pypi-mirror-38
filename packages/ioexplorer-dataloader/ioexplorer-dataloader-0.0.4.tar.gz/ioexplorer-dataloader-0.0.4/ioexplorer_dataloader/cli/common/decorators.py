import os
import json
from functools import wraps
from sqlalchemy import create_engine
from .logging import error, info

def add_env_variables(func):
    @wraps(func)
    def add_env(*args, **kwargs):
        env = {}
        if 'IOEXPLORER_MODE' in os.environ:
            env['mode'] = os.environ['IOEXPLORER_MODE']
        else:
            info('`IOEXPLORER_MODE` environment variable was not set. Defaulting to "development".')
            env['mode'] = 'development'
        if env['mode'] in ['production', 'development', 'testing']:
            prefix = 'IOEXPLORER_{}'.format(env['mode'].upper())
            for var in ['DATABASE_NAME',
                        'DATABASE_HOST',
                        'DATABASE_PORT',
                        'DATABASE_USERNAME',
                        'DATABASE_PASSWORD',
                        ]:
                env_var = '_'.join([prefix, var])
                try:
                    env[var.lower()] = os.environ[env_var] 
                except KeyError:
                    error("The `{}` environment variable was not set. Exiting.".format(env_var))
        else:
            error('The `IOEXPLORER_MODE` environment variable is not set properly. '
                'It should be one of ["production", "development", "testing"]')
        return func(*args, _env=env, **kwargs)
    return add_env


def connect_to_db(func):
    @wraps(func)
    def connect_then_run(_env, **kwargs):
        engine = create_engine(
            "postgres://{database_username}:{database_password}@"
            "{database_host}:{database_port}/{database_name}"
            .format(**_env),
            paramstyle='format'
        )
        conn = engine.connect()
        return func(conn=conn, engine=engine, _env=_env,  **kwargs)
    return connect_then_run