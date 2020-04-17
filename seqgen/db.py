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
    db = g.pop('db', None)

    if db is not None:
        db.connection.close()


def init_db():
    """
        Initialise the required database components.
    """
    current_app.logger.debug('init_db()')
    db = get_db()

    with db.connection:
        with db.cursor as cursor:
            sequence_name = current_app.config.sequence_name
            cursor.execute(
                f"SELECT sequence_name \
                  FROM information_schema.sequences \
                  WHERE sequence_name='{sequence_name}';")
            seq_check = cursor.fetchone()

            if not seq_check:
                current_app.logger.debug(f'Creating the sequence: {sequence_name}')
                cursor.execute(
                    f'CREATE SEQUENCE {sequence_name} START {current_app.config.sequence_start};'
                )

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

    return str(result[0])


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
