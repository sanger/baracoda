# flake8: noqa
from typing import Sequence
from baracoda.config.defaults import *
from baracoda.formats.generic import GenericBarcodeFormatter
from baracoda.formats.sequencescape import Sequencescape22Formatter

# Adds a development prefix for sqp sequence
PREFIXES.append(
    {
        "prefix": "SQPD",
        "sequence_name": "sqp",
        "formatter_class": Sequencescape22Formatter,
        "enableChildrenCreation": True,
    }
)

# settings here overwrite those in 'defaults.py'

# adding an additional barcode prefix for use in source plate data setup
# for beckman and biosero, sharing the ht sequence
PREFIXES.append(
    {
        "prefix": "TEST",
        "sequence_name": "ht",
        "formatter_class": GenericBarcodeFormatter,
        "enableChildrenCreation": False,
    }
)
