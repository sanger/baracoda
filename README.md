# baracoda
Generate barcodes on demand

## How to set up a development environment

1. Install postgresql

```bash
brew install postgresql
```

2. Configure Postgresql:

To configure postgresql database for the project you only need to create the database and add a user to access it. For example, to create the databases baracoda_dev and baracoda_test and create the user postgres with password postgres to access them:

```bash
(baracoda) bash-3.2$ psql
psql (12.2)
Type "help" for help.
=# create database baracoda_dev;
CREATE DATABASE
=# create database baracoda_test;
CREATE DATABASE
=# create user postgres with encrypted password 'postgres';
CREATE ROLE
=# grant all privileges on database baracoda_dev to postgres;
GRANT
=# grant all privileges on database baracoda_test to postgres;
GRANT
```

3. Create a .env file with the database and environment configuration for the environment we want to run. For example, for a development environment we could use:

```python
FLASK_APP=baracoda
FLASK_ENV=development
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_DBNAME=baracoda_dev
```

4. Install the python libraries with pipenv:

```bash
# pipenv install
```

5. Run the pipenv shell

```bash
# pipenv shell
```

6. Initialize the database and create required sequences (only needed when we change the config/settings.py):

```bash
# flask init-db
```

7. Start the app:
```bash
# flask run
```

## Running the tests

Run the following command inside a pipenv shell:
```bash
python -m pytest
```