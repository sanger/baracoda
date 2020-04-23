import os
import sys
from werkzeug.utils import import_string

required_config = ('db_host', 'db_port', 'db_user', 'db_password', 'db_dbname')

def load_config(app, config):
    current_env = get_current_env(config)

    if current_env == 'development':
        load_env_config(app)
        app.config.update(import_string('config.settings.development_config')())

    if current_env == 'test':
        load_mapping_config(app, config)
        app.config.update(import_string('config.settings.testing_config')())
        
    if current_env == 'production':
        load_env_config(app)
        app.config.update(import_string('config.settings.production_config')())

def get_current_env(config):
    if config is None:
        return os.getenv('FLASK_ENV')
    else:
        return 'test'

def validate_config(app):
    for config in required_config:
        if not config in app.config.__dict__.keys():
            sys.exit(f'The required config parameter is missing: {config}')

def load_mapping_config(app, mapping):
    for config in mapping:
        setattr(app.config, config.lower(), mapping[config])
    
    validate_config(app)        

def load_env_config(app):
    for config in required_config:
        setattr(app.config, config.lower(), os.getenv(config.upper()))

    validate_config(app)
