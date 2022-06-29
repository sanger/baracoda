# Baracoda

![CI](https://github.com/sanger/baracoda/workflows/CI/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/sanger/baracoda/branch/develop/graph/badge.svg)](https://codecov.io/gh/sanger/baracoda)

Barcode generation using postgres sequences and pre-defined prefixes.

## Features

Baracoda is a JSON-based microservice written in Python and backed in a
PostgreSQL database, with the purpose of handling the creation
of new barcodes for the LIMS application supported currently in PSD.

These are some of the key features currently supported:

* Creation of single barcodes
* Creation of group of barcodes
* Support for children barcodes creation
* Retrieval of the last barcode created for a prefix
* Support for different barcode formats

## Table of Contents

<!-- toc -->

- [Requirements for Development](#requirements-for-development)
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
- [Configuration](#configuration)
  * [Formatter classes](#formatter-classes)
  * [Children barcode creation](#children-barcode-creation)
- [Troubleshooting](#troubleshooting)
  * [Installing psycopg2](#installing-psycopg2)
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
- Git hooks are executed using [lefthook](https://github.com/evilmartians/lefthook), install
  lefthook using homebrew and add the pre-commit and pre-push hooks as follows:

      lefthook add pre-commit
      lefthook add pre-push
- [talisman](https://github.com/thoughtworks/talisman) is used as a credentials checker, to ignore
  files which it triggers as false positives, follow the instructions in the git commit output by
  adding the files to be ignore to a `.talismanrc` file and try commit again.

### Setup Steps

1. Create and enter the virtual environment:

        pipenv shell

1. Install the required dependencies:

        pipenv install --dev

    See the [Troubleshooting](#troubleshooting) section for any commonly encountered installation issues.

1. Create the required sequences and tables:

        flask init-db

1. Run the migrations:

        flask db upgrade

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

      flask db revision --autogenerate -m "Added account table"

## Routes

The following routes are available from this service:

    flask routes

    Endpoint                                Methods  Rule
    --------------------------------------  -------  ----------------------------
    barcode_creation.get_last_barcode       GET      /barcodes/<prefix>/last
    barcode_creation.get_new_barcode        POST     /barcodes/<prefix>/new
    barcode_creation.get_new_barcode_group  POST     /barcodes_group/<prefix>/new
    child_barcodes.new_child_barcodes       POST     /child-barcodes/<prefix>/new
    health_check                            GET      /health
    static                                  GET      /static/<path:filename>

## Configuration

The default configuration of the currently supported prefixes is specified in the
```baracoda/config/defaults.py``` module. For example:
```json
    {
        "prefix": "HT",
        "sequence_name": "ht",
        "formatter_class": GenericBarcodeFormatter,
        "enableChildrenCreation": False,
    }
```
These are the allowed keywords that we can specify to configure a prefix:

- ```prefix```: This is the string that represents the prefix we are configuring for
supporting new barcodes.
- ```sequence_name```: This is the sequence name in the PostgreSQL database which will
keep record of the last index created for a barcode. Prefixes can share the same
sequence.
- ```formatter_class```: Defines the class that will generate the string that represents
a new barcode by using the prefix and the new value obtained from the sequence.
If we want to support a new formatter class we have to provide a class that implements
the interface ```baracoda.formats.FormatterInterface```.
- ```enableChildrenCreation```: Defines if the prefix has enabled the children creation.
If true, the prefix will support creating barcodes based on a parent barcode
If it is False, the prefix will reject any children creation request for that prefix.


### Formatter classes

A formatter class is a way of rendering a new barcode created that can be attached to a prefix
through the configuration before. Any new Formatter class must extend from the abstract class
```baracoda.formats.FormatterInterface```.

The current list of supported formatter classes that can be specified for a prefix is:

- HeronCogUkIdFormatter
- GenericBarcodeFormatter
- Sequencescape22Formatter


#### HeronCogUkIdFormatter

Implements the Heron COG UK Id generation that corresponds with format: ```<Prefix>-<Hexadecimal><Checksum>```.
Examples: ```ASDF-A34ADA```

With description:

- Prefix is the prefix provided to the formatter.
- Hexadecimal is the hexadecimal representation for the current index for the id.
- Checksum is a checksum hexadecimal character that validates the hexadecimal value.

#### GenericBarcodeFormatter

Standard barcode generator that follows the format: ```<Prefix>-<Number>```.
Examples: ```HT-11811```

With description:

- Prefix is the prefix provided to the formatter
- Number is the current index for the id of this barcode.

#### Sequencescape22Formatter

Plate barcode generator which supports children creation and checksum. It follows these 2 formats:
 - For any barcode that is not a children: ```<Prefix>-<Number>-<Checksum>```. Examples: ```SQDP-23-L```
 - For any children barcode: ```<Prefix>-<Number>-<ChildIndex>-<Checksum>```. Examples: ```LAB-89-2-R```

With description:

- Prefix is the prefix provided to the formatter
- Number is the current index for the id of this barcode.
- ChildIndex is the current index for the child (if is a children barcode).
- Checksum is a checksum letter that validates the whole barcode (prefix, number, childIndex).


### Children barcode creation

This section only applies to the barcode formatters that support children barcode creation
which currently only happens with ```Sequencescape22Formatter```.

Children barcodes from a parent barcode can be created with a POST request to the
endpoint with a JSON body:

```/child-barcodes/<PREFIX/new```

The inputs for this request will be:

- *Prefix* : prefix where we want to create the children under. This argument will be
extracted from the URL ```/child-barcodes/<PREFIX>/new```
All barcodes for the children will have this prefix (example, prefix SS will generate children
like SS-11111-1-L, SS-11111-2-M, etc)
- *Parent Barcode* : barcode that will act as parent of the children. This argument will be
extracted from the Body of the request, eg: ```{'barcode': 'SS-1-1-L', 'count': 2}```.
To be considered valid, the barcode needs to follow the format ```<PREFIX>-<NUMBER>(-<NUMBER>)?(-<CHECKSUM>)```
where the second number part is optional and it represents if the barcode was a child.
For example, valid barcodes would be ```SS-11111-13-M``` (normal parent) and ```SS-11112-24-N```
(parent that was a child) but not ```SS-1-1-1-L``` (several '-') or ```SS12341-1-L``` (no '-' separation).
- *Child* : part of the Parent barcode string that would identify if the parent was
a child before (the last number). For example for the *Parent barcode* ```SS-11111-14-R```,
*Child* would be 14; but for the *Parent barcode* ```SS-11111-W```, *Child* would have no
value defined.
- *Count* : number of children barcodes to create.

#### Wrong parent barcodes

A request with parent barcode that does not follow the format defined like:
```
<PREFIX>-<NUMBER>(-<NUMBER>)?(-<CHECKSUM>)
```
will create normal barcodes instead of suffixed children barcodes (normal barcode creation).

A request that follows the right format but does not comply with current database will be
rejected as impostor barcode. For example, if we receive the parent barcode ```SS-1111-14-N```, but in the
database the parent ```SS-1111-R``` has only created 12 child barcodes yet, so ```SS-1111-14-N``` is
impossible to have been generated by Baracoda.

#### Child Barcode Generation Logic Workflow

The following diagram describes the workflow of how this endpoint will behave depending on
the inputs declared before:


```mermaid
graph TD;
  Prefix(Prefix is extracted from URL) --> PrefixEnabled[[Is 'Prefix' enabled by config to create children]];
  ParentBarcode(Parent barcode is extracted from URL arg) --> PrefixEnabled[[Is 'Prefix' enabled by config to create children]];
  Child(Child is extracted from Parent barcode) --> PrefixEnabled[[Is 'Prefix' enabled by config to create children]];
  PrefixEnabled -->|Yes|ValidBarcode[[Is 'Parent Barcode' a valid parent?]];
  PrefixEnabled -->|No|Rejected([HTTP 422 - Rejected]);
  ValidBarcode -->|Yes|ParentPresent[[Is 'Parent barcode' present in database?]];
  ValidBarcode -->|No|NormalBarcode(Generate normal barcodes for the Prefix);
  NormalBarcode -->NormalAccept([HTTP 201 - Created])
  ParentPresent -->|Yes|ChildExist[[Do we have a value for 'Child'?]];
  ParentPresent -->|No|ChildExist2[[Do we have a value for 'Child'?]];
  ChildExist -->|Yes|ChildConstraint[[Is 'Child' bigger than the last child generated by the 'Parent barcode' in previous requests?]];
  ChildConstraint -->|Yes|Impostor([HTTP 500 - Parent barcode is an impostor]);
  ChildExist2 -->|Yes|Impostor;
  ChildExist -->|No|ChildrenBarcodes(Generate children barcodes);
  ChildrenBarcodes --> NormalAccept;
  ChildConstraint -->|No|ChildrenBarcodes
  ChildExist2 -->|No|ChildrenBarcodes;

```

### Troubleshooting

#### Installing psycopg2

If errors are experienced while pipenv attempts to install `psycopg2`, try this:

    LDFLAGS=`echo $(pg_config --ldflags)` pipenv install --dev

You can also try installing `psycopg2` from the binary, which avoids the need for `pg_config` locally.
To install `psycopg2` as a binary, change the `psycopg2` entry in the Pipfile to say `psycopg2-binary` instead, and then run:

    pipenv install psycopg2-binary

You can then run `pipenv install --dev` again to get all the other dependencies installed.
This approach should allow you to install the postgres python driver (psycopg2) locally, without having a local copy of postgres. Use docker to run postgres as described in the 'Requirements for Development' section.
Don't commit your changes to the Pipfile or Pipfile.lock.

### Updating the Table of Contents

To update the table of contents after adding things to this README you can use the [markdown-toc](https://github.com/jonschlinkert/markdown-toc)
node module. To run:

    npx markdown-toc -i README.md
