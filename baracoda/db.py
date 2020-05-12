import logging
from collections import namedtuple

import click
import psycopg2  # type: ignore
from sqlalchemy.orm import sessionmaker
from flask import current_app, g
from flask.cli import with_appcontext

from sqlalchemy import create_engine

SCHEMA_FILE = "baracoda/sql/schema.sql"

logger = logging.getLogger(__name__)


def get_db_uri():
    user = current_app.config["DB_USER"]
    password = current_app.config["DB_PASSWORD"]
    host = current_app.config["DB_HOST"]
    port = current_app.config["DB_PORT"]
    dbname = current_app.config["DB_DBNAME"]
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"


def get_db():
    logger.debug("Getting a connection to the database")

    if "db" not in g:
        Database = namedtuple("Database", ["session", "engine"])

        engine = create_engine(get_db_uri(), echo=True)
        session = sessionmaker(bind=engine)

        g.db = Database(session, engine)

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

    session = db.session()
    session.execute(schema_loader)
    session.commit()


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database")


def init_app(app):
    # app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
