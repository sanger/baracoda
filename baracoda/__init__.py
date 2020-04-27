import logging
import logging.config
import os

from flask import Flask

from baracoda import barcodes, db
from baracoda.logging_conf import LOGGING_CONF

logger = logging.getLogger(__name__)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)

    if test_config is None:
        # load the config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    logging.config.dictConfig(LOGGING_CONF)
    logger.error("test")

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    app.register_blueprint(barcodes.bp)

    @app.route("/hello")
    def hello():
        logger.debug("hello")
        logger.error("hello")
        try:
            raise Exception("testing")
        except Exception as e:
            pass
        return "hello world"

    return app
