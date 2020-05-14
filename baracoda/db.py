import logging
from collections import namedtuple

import click
from flask import current_app, g
from flask.cli import with_appcontext

from flask_sqlalchemy import SQLAlchemy  # type: ignore


SCHEMA_FILE = "baracoda/sql/schema.sql"

logger = logging.getLogger(__name__)


db = SQLAlchemy()


def reset_db():
    """
        Initialise the required database components.
    """
    logger.debug("init_db()")

    with open(SCHEMA_FILE, "r") as schema_file:
        # schema_loader = "".join(schema_file.readlines())
        schema_loader = schema_file.read()

    db.session.execute(schema_loader)
    db.session.commit()
