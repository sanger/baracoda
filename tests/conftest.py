import pytest

from baracoda import create_app
from baracoda.barcode_formats import HeronFormatter
from baracoda.db import init_db


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
        }
    )

    with app.app_context():
        init_db()  # Create the test schema

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def heron_formatter():
    return HeronFormatter(prefix="SANG")
