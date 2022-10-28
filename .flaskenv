# use publicly acessible env variables in this file
#   https://flask.palletsprojects.com/en/2.2.x/cli/#environment-variables-from-dotenv

# https://flask.palletsprojects.com/en/2.2.x/cli/#application-discovery
FLASK_APP=baracoda

# https://flask.palletsprojects.com/en/2.2.x/cli/#setting-command-options
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=8000

# https://flask.palletsprojects.com/en/2.2.x/config/#DEBUG
FLASK_DEBUG=true

# path to the settings file which flask will use
SETTINGS_PATH=config/development.py
