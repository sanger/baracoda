import os
import sys

required_config = ('db_host', 'db_port', 'db_user', 'db_password', 'db_dbname', 'sequence_name',
                       'sequence_start')

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
