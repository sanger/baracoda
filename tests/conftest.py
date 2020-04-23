import pytest
from baracoda import create_app
from baracoda.db import init_db
import click

@click.command()
@click.option('--test-from-folder', default=".", help='Folder that contains .csv files to test.')
def test_from_folder():
    pass

@pytest.fixture
def app():
    app = create_app(
        {
            "DB_HOST":"localhost",
            "DB_PORT":5432,
            "DB_USER":"postgres",
            "DB_PASSWORD":"postgres",
            "DB_DBNAME":"baracoda_test"
        }
    )

    with app.app_context():
        init_db()  # Create the test schema

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
