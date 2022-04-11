# flake8: noqa
from baracoda.config.defaults import *
from baracoda.formats import GenericBarcodeFormatter

# Adds a development prefix for sqp sequence
PREFIXES.append({"prefix": "SQPD", "sequence_name": "sqp", "formatter_class": GenericBarcodeFormatter})

# settings here overwrite those in 'defaults.py'

# adding an additional barcode prefix for use in source plate data setup
# for beckman and biosero, sharing the ht sequence
PREFIXES.append({"prefix": "TEST", "sequence_name": "ht", "formatter_class": GenericBarcodeFormatter})
