import os
import sys


def load_config(app):
    required_config = ('DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASSWORD', 'DB_DBNAME', 'SEQUENCE_NAME',
                       'SEQUENCE_START')
    for config in required_config:
        if (conf := os.getenv(config)):
            setattr(app.config, config.lower(), conf)
        else:
            sys.exit(f'The required config parameter is missing from ENV: {config}')
