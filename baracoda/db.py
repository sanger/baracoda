import logging
import types
from collections import namedtuple
from typing import Dict, NamedTuple

import click
import psycopg2  # type: ignore
from flask import current_app, g
from flask.cli import with_appcontext

SCHEMA_FILE = "baracoda/sql/schema.sql"

logger = logging.getLogger(__name__)


def get_db():
    logger.debug("Getting a connection to the database")

    if "db" not in g:
        Database = namedtuple("Database", ["connection", "cursor"])

        connection = psycopg2.connect(
            user=current_app.config["DB_USER"],
            password=current_app.config["DB_PASSWORD"],
            host=current_app.config["DB_HOST"],
            port=current_app.config["DB_PORT"],
            dbname=current_app.config["DB_DBNAME"],
        )

        cursor = connection.cursor()

        g.db = Database(connection, cursor)

    return g.db


def close_db(e=None) -> None:
    """
    Close the connection to the database.
    """
    db_obj = g.pop("db", None)

    if db_obj is not None:
        db_obj.connection.close()


def init_db():
    """
        Initialise the required database components.
    """
    logger.debug("init_db()")
    db = get_db()

    with open(SCHEMA_FILE, "r") as schema_file:
        # schema_loader = "".join(schema_file.readlines())
        schema_loader = schema_file.read()

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
