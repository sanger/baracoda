# flake8: noqa
from baracoda.config.defaults import *
from baracoda.formats import GenericBarcodeFormatter

# Adds a development prefix for sqp sequence
PREFIXES.append({"prefix": "SQPD", "sequence_name": "sqp", "formatter_class": GenericBarcodeFormatter})

# settings here overwrite those in 'defaults.py'
