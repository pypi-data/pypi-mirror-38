import os
import json
from functools import wraps
from sqlalchemy import create_engine
from .logging import error

def read_conf(func):
    @wraps(func)
    def read(database_name, database_config, **kwargs):
        conf_path = os.path.join(database_config, '{}.config.json'.format(database_name))
        if os.path.exists(conf_path):
            with open(conf_path, 'r') as f:
                conf = json.load(f)
        else:
            error("I could not find a database config file at {}".format(conf_path))
        return func(database_name=database_name, conf=conf, **kwargs)
    return read


def connect_to_db(func):
    @wraps(func)
    def connect_then_run(database_name, conf, **kwargs):
        engine = create_engine(
            "{dialect}://{username}:{password}@{host}:{port}/{database}".format(**conf),
            paramstyle='format'
        )
        conn = engine.connect()
        return func(conn=conn, engine=engine, name=database_name, **kwargs)
    return connect_then_run