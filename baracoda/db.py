import logging

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

SCHEMA_FILE = "baracoda/sql/schema.sql"

logger = logging.getLogger(__name__)


db = SQLAlchemy()


def reset_db():
    """
    Initialise the required database components.
    """
    logger.debug("init_db()")

    with open(SCHEMA_FILE, "r") as schema_file:
        schema_loader = schema_file.read()

    db.session.execute(text(schema_loader))
    db.session.commit()
