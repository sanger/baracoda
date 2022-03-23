# flake8: noqa
from baracoda.config.defaults import *

# settings here overwrite those in 'defaults.py'
###
# Flask config
###
TESTING = True

###
# database config
###
DB_DBNAME = "baracoda_test"
DB_HOST = "host.docker.internal"
SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DBNAME}"
