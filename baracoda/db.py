import psycopg2
import types

import click
from flask import current_app, g
from flask.cli import with_appcontext
from datetime import datetime
from werkzeug.utils import import_string

SCHEMA_FILE = "baracoda/sql/schema.sql"


def get_db():
    if "db" not in g:
        g.db = types.SimpleNamespace()
        g.db.connection = psycopg2.connect(
            user=current_app.config.db_user,
            password=current_app.config.db_password,
            host=current_app.config.db_host,
            port=current_app.config.db_port,
            dbname=current_app.config.db_dbname,
        )
        g.db.cursor = g.db.connection.cursor()

    return g.db


def close_db(e=None):
    """
    Close the connection to the database.
    """
    db_obj = g.pop("db", None)

    if (db_obj is not None) and ("connection" in db_obj.__dict__.keys()):
        db_obj.connection.close()


def init_db():
    """
        Initialise the required database components.
    """

    current_app.logger.debug("init_db()")
    db = get_db()

    with open(SCHEMA_FILE, "r") as myfile:
        schema_loader = "".join(myfile.readlines())

    with db.connection:
        with db.cursor as cursor:
            cursor.execute(schema_loader)


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
