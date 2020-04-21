import os, json
from flask import Flask
from baracoda import utils, db, barcode_creation

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        #app.config.from_pyfile("config.py", silent=True)
        utils.load_env_config(app)
        #utils.load_file_config(app, "")
    else:
        utils.load_mapping_config(app, test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    app.register_blueprint(barcode_creation.bp)

    return app
