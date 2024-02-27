import logging
import logging.config
from http import HTTPStatus

import click
from flask import Flask, Request
from flask.cli import with_appcontext

from baracoda import barcodes
from baracoda import child_barcodes
from baracoda.config.logging import LOGGING
from baracoda.db import db, reset_db
from flask_migrate import Migrate

logger = logging.getLogger(__name__)


@click.command("init-db")
@with_appcontext
def init_db_command():
    reset_db()
    click.echo("Reseting the database")


class SubRequest(Request):
    """
    A subclass to mitigate the forcing of application/json header
    """

    @property
    def json(self):
        return self.get_json(force=True)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)

    # Overrides the default Request class with a request class that does not force application/json header
    # for request.json call
    app.request_class = SubRequest

    if test_config is None:
        # load the config, if it exists, when not testing
        # app.config.from_pyfile("config.py", silent=True)
        app.config.from_envvar("SETTINGS_PATH")
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    Migrate(app, db)

    logging.config.dictConfig(LOGGING)

    app.cli.add_command(init_db_command)

    app.register_blueprint(barcodes.bp)
    app.register_blueprint(child_barcodes.bp)

    @app.route("/health")
    def health_check():
        return "Factory working", HTTPStatus.OK

    return app
