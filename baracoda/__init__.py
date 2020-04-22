import os, json
from flask import Flask
from baracoda import db, barcode_creation
from config.loader import load_config

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    load_config(app, test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    app.register_blueprint(barcode_creation.bp)

    return app
