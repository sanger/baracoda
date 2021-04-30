# Baracoda

![CI](https://github.com/sanger/baracoda/workflows/CI/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/sanger/baracoda/branch/develop/graph/badge.svg)](https://codecov.io/gh/sanger/baracoda)

Barcode generation using postgres sequences and pre-defined prefixes.

## Table of Contents

<!-- toc -->

- [Requirements for Development](#requirements-for-development)
  * [Configuring Environment](#configuring-environment)
  * [Setup Steps](#setup-steps)
- [Running](#running)
- [Testing](#testing)
  * [Testing Requirements](#testing-requirements)
  * [Running Tests](#running-tests)
- [Formatting, Linting and Type Checking](#formatting-linting-and-type-checking)
  * [Formatting](#formatting)
  * [Linting](#linting)
  * [Type Checking](#type-checking)
- [Deployment](#deployment)
- [Autogenerating Migrations](#autogenerating-migrations)
- [Routes](#routes)
- [Miscellaneous](#miscellaneous)
  * [Troubleshooting](#troubleshooting)
    + [Installing psycopg2](#installing-psycopg2)
  * [Updating the Table of Contents](#updating-the-table-of-contents)

<!-- tocstop -->

## Requirements for Development

The following tools are required for development:

- python (use `pyenv` or something similar to install the python version specified in the `Pipfile`)
- postgresql server and `pg_config` library
  - if using homebrew (this will install both the server and library):

        brew install postgresql@9.6
        brew link postgresql@9.6 --force

    Create the development database and user using a RDBMS GUI or by running this query in a client:

        create database baracoda_dev;
        grant all privileges on database baracoda_dev to postgres;

  - to spin up a server using Docker (the `pg_config` library will still be needed by the
application), use the `docker-compose.yml` file:

        docker compose up -d

    The compose service automatically creates the `baracoda_dev` database and `postgres` user.

### Configuring Environment

Create a `.env` file (or copy the `.env.example` file) with the following values:

    SETTINGS_PATH=config/development.py

### Setup Steps

1. Create and enter the virtual environment:

        pipenv shell

1. Install the required dependencies:

        pipenv install --dev

    See the [Troubleshooting](#troubleshooting) section for any commonly encountered installation issues.

1. Create the required sequences and tables:

        flask init-db

1. Run the migrations:

        alembic upgrade head

## Running

To run the service:

    flask run

## Testing

### Testing Requirements

The test suite requires a test database, currently named `baracoda_test`.

Create the database using a RDBMS GUI or by running this query in a client:

    create database baracoda_test;
    grant all privileges on database baracoda_test to postgres;

### Running Tests

To run the test suite:

    python -m pytest -vx

## Formatting, Linting and Type Checking

### Formatting

This project is formatted using [black](https://github.com/psf/black). To run formatting checks,
run:

    pipenv run black .

### Linting

This project is linted using [flake8](https://github.com/pycqa/flake8). To lint the code, run:

    pipenv run flake8

### Type Checking

This project uses static type checking provided by the [mypy](https://github.com/python/mypy)
library, to run manually:

    pipenv run mypy .

## Deployment

This project uses a Docker image as the unit of deployment. The image is created by GitHub actions.
To trigger the creation of a new image, increment the `.release-version` version with the
corresponding change according to [semver](https://semver.org/).

## Autogenerating Migrations

- Make sure your local database is up to date with last schema available
- Perform any change in the models files located in the `baracoda/orm` folder
- Run alembic and provide a comment to autogenerate the migration comparing with current database:

      alembic revision --autogenerate -m "Added account table"

## Routes

The following routes are available from this service:

    flask routes

    Endpoint                                Methods  Rule
    --------------------------------------  -------  ----------------------------
    barcode_creation.get_last_barcode       GET      /barcodes/<prefix>/last
    barcode_creation.get_new_barcode        POST     /barcodes/<prefix>/new
    barcode_creation.get_new_barcode_group  POST     /barcodes_group/<prefix>/new
    health_check                            GET      /health
    static                                  GET      /static/<path:filename>

## Miscellaneous

### Troubleshooting

#### Installing psycopg2

If errors are experienced while pipenv attempts to install `psycopg2`, try this:

    LDFLAGS=`echo $(pg_config --ldflags)` pipenv install --dev

### Updating the Table of Contents

To update the table of contents after adding things to this README you can use the [markdown-toc](https://github.com/jonschlinkert/markdown-toc)
node module. To run:

    npx markdown-toc -i README.md
