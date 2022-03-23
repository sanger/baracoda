# flake8: noqa
from baracoda.config.defaults import *

# settings here overwrite those in 'defaults.py'

# adding an additional barcode prefix for use in source plate data setup
# for beckman and biosero, sharing the ht sequence
PREFIXES.append({"prefix": "TEST", "sequence_name": "ht", "convert": False})
