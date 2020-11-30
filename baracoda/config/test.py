from baracoda.config.defaults import *

# settings here overwrite those in 'defaults.py'
TESTING = True
FLASK_ENV = "test"
DB_DBNAME = "baracoda_test"
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:postgres@localhost:5432/baracoda_test"