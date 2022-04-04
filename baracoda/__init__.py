import logging
import logging.config
from http import HTTPStatus

import click
from flask import Flask
from flask.cli import with_appcontext

from baracoda import barcodes
from baracoda.config.logging import LOGGING
from baracoda.db import db, reset_db

logger = logging.getLogger(__name__)


@click.command("init-db")
@with_appcontext
def init_db_command():
    reset_db()
    click.echo("Reseting the database")


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)

    if test_config is None:
        # load the config, if it exists, when not testing
        # app.config.from_pyfile("config.py", silent=True)
        app.config.from_envvar("SETTINGS_PATH")
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    logging.config.dictConfig(LOGGING)

    app.cli.add_command(init_db_command)

    app.register_blueprint(barcodes.bp)

    @app.route("/health")
    def health_check():
        return "Factory working", HTTPStatus.OK

    return app
