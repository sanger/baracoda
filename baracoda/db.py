import psycopg2
import types

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = types.SimpleNamespace()
        g.db.connection = psycopg2.connect(
            user=current_app.config.db_user,
            password=current_app.config.db_password,
            host=current_app.config.db_host,
            port=current_app.config.db_port,
            dbname=current_app.config.db_dbname
        )
        g.db.cursor = g.db.connection.cursor()

    return g.db


def close_db(e=None):
    """
    Close the connection to the database.
    """
    db_obj = g.pop('db', None)

    if (db_obj is not None) and ('connection' in db_obj.__dict__.keys()):
        db_obj.connection.close()


def exists_sequence(cursor, sequence_name):
    cursor.execute(
        f"SELECT sequence_name \
            FROM information_schema.sequences \
            WHERE sequence_name='{sequence_name}';")
    seq_check = cursor.fetchone()
    return seq_check

def create_sequence(cursor, sequence_name, sequence_start):
    current_app.logger.debug(f'Creating the sequence: {sequence_name}')
    cursor.execute(
        f'CREATE SEQUENCE {sequence_name} START {sequence_start};'
    )

def reset_sequence_to_value(cursor, sequence_name, sequence_start):
    cursor.execute(f'ALTER SEQUENCE {sequence_name} RESTART WITH {sequence_start};')

def init_db():
    """
        Initialise the required database components.
    """
    current_app.logger.debug('init_db()')
    db = get_db()

    with db.connection:
        with db.cursor as cursor:
            sequence_name = current_app.config.sequence_name
            sequence_start = current_app.config.sequence_start

            if not exists_sequence(cursor, sequence_name):
                create_sequence(cursor, sequence_name, sequence_start)
            
            if (current_app.config.reset_sequence == True):
                reset_sequence_to_value(cursor, sequence_name, sequence_start)                


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database')


def get_next_value():
    db = get_db()
    with db.cursor as cursor:
        cursor.execute(f"SELECT nextval('{current_app.config.sequence_name}');")
        result = cursor.fetchone()

    return result[0]


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)