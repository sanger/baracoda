import os
import sys
from baracoda import utils
from werkzeug.utils import import_string

required_config = ('db_host', 'db_port', 'db_user', 'db_password', 'db_dbname', 'sequence_name',
                       'sequence_start')

def load_config(app, config):
    if config is None:
        utils.load_env_config(app)
    else:
        utils.load_mapping_config(app, config)

    load_settings(app)

def load_settings(app):
    current_env = os.getenv('FLASK_ENV')

    if current_env == 'development':
        app.config.update(import_string('config.settings.development_config')())

    if current_env == 'test':
        app.config.update(import_string('config.settings.testing_config')())
        
    if current_env == 'production':
        app.config.update(import_string('config.settings.production_config')())

def validate_config(app):
    for config in required_config:
        if not config in app.config.__dict__.keys():
            sys.exit(f'The required config parameter is missing: {config}')

def load_mapping_config(app, mapping):
    for config in mapping:
        setattr(app.config, config.lower(), mapping[config])
    
    validate_config(app)        

def load_file_config(app, file):
    app.config.from_pyfile("config.py", silent=True)
    
    validate_config(app)        

def load_env_config(app):
    for config in required_config:
        setattr(app.config, config.lower(), os.getenv(config.upper()))

    validate_config(app)
