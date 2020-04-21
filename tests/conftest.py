import pytest
from baracoda import create_app
from baracoda.db import init_db

@pytest.fixture
def app():
    app = create_app(
        {
            "RESET_SEQUENCE": True,
            "DB_HOST":"localhost",
            "DB_PORT":5432,
            "DB_USER":"postgres",
            "DB_PASSWORD":"",
            "DB_DBNAME":"baracoda_test",
            "SEQUENCE_NAME":"heron",
            "SEQUENCE_START":1
        }
    )

    with app.app_context():
        init_db()  # Create the test schema

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
