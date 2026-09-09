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
    # Split SQL statements by semicolon for MySQL compatibility
    statements = [stmt.strip() for stmt in schema_loader.split(";") if stmt.strip()]

    for statement in statements:
        try:
            db.session.execute(text(statement))
        except Exception as e:
            logger.error(f"Error executing statement: {statement}\n{e}")
            raise
    db.session.commit()
