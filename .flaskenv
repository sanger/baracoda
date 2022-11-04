# use publicly acessible env variables in this file
#   https://flask.palletsprojects.com/en/1.1.x/cli/#environment-variables-from-dotenv

# https://flask.palletsprojects.com/en/1.1.x/cli/#application-discovery
FLASK_APP=baracoda

# https://flask.palletsprojects.com/en/1.1.x/cli/#setting-command-options
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=7900

# https://flask.palletsprojects.com/en/1.1.x/config/#environment-and-debug-features
FLASK_ENV=development

# path to the settings file which flask will use
SETTINGS_PATH=config/development.py
