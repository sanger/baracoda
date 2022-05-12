import pytest

from baracoda import create_app
from baracoda.db import db, reset_db
from baracoda.formats import HeronCogUkIdFormatter
from baracoda.helpers import get_prefix_item
from baracoda.constants import ENABLE_CHILDREN_CREATION

from tests.data.fixture_data import PREFIXES
from unittest.mock import patch


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
    return HeronCogUkIdFormatter(prefix="SANG")


@pytest.fixture
def prefixes():
    return PREFIXES


@pytest.fixture
def enable_children_for_prefix(app, prefix):
    with app.app_context():
        item = get_prefix_item(prefix)
        item[ENABLE_CHILDREN_CREATION] = True
        with patch("baracoda.operations.get_prefix_item", return_value=item):
            yield
