import pytest

from baracoda import create_app
from baracoda.db import db, reset_db
from baracoda.formats import HeronFormatter

from tests.data.fixture_data import PREFIXES


@pytest.fixture
def app():
    app = create_app(
        {
            "DB_HOST": "localhost",
            "DB_PORT": 5432,
            "DB_USER": "postgres",
            "DB_PASSWORD": "postgres",
            "DB_DBNAME": "baracoda_test",
            "SEQUENCE_NAME": "heron",
            "SEQUENCE_START": "200000",
            "SEQUENCE_RESET": True,
            "SLACK_API_TOKEN": "",
            "SLACK_CHANNEL_ID": "",
            "SQLALCHEMY_DATABASE_URI": "postgresql+psycopg2://postgres:postgres@localhost:5432/baracoda_test",
            "PREFIXES": PREFIXES,
        }
    )

    with app.app_context():
        db.init_app(app)  # Create the test schema
        reset_db()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def heron_formatter():
    return HeronFormatter(prefix="SANG")


@pytest.fixture
def prefixes():
    return PREFIXES
