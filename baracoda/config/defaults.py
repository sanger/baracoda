from typing import List

from baracoda.formats.generic import GenericBarcodeFormatter
from baracoda.formats.heron import HeronCogUkIdFormatter
from baracoda.types import PrefixesType

###
# database config
###
DB_DBNAME = "baracoda_dev"
DB_HOST = "host.docker.internal"
DB_PASSWORD = "postgres"
DB_PORT = "5432"
DB_USER = "postgres"
SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DBNAME}"

###
# sequence config
###
SEQUENCE_NAME = "heron"
SEQUENCE_START = "200000"

###
# slack config
###
SLACK_API_TOKEN = "xoxb-123"
SLACK_CHANNEL_ID = "Cxxx"

###
# prefix for barcodes returned from the respective sequece
###

PREFIXES: List[PrefixesType] = [
    {
        "prefix": "ALDP",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "BHRT",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "BIRM",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "BRBR",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "BRIG",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "BRIS",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "CAMB",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "CAMC",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "CCCU",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "CPTD",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "CWAR",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "EDIN",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "EKHU",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "EXET",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "GCVR",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "GLOU",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "GSTT",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "HECH",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "HSLL",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "KGHT",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "LCST",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "LEED",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "LIVE",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "LOND",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "LSPA",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "MILK",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "MTUN",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "NEWC",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "NIRE",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "NORT",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "NORW",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "NOTT",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "NWGH",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "OXON",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "PAHT",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "PHEC",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "PHWC",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "PLYM",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "PORT",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "PRIN",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "QEUH",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "RAND",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "RSCH",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "SANG",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "SHEF",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "TBSD",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "TFCI",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "WAHH",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "WSFT",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "WSI",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "CBAG",
        "sequence_name": "csm",
        "formatter_class": GenericBarcodeFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "CBOX",
        "sequence_name": "csm",
        "formatter_class": GenericBarcodeFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "CEPS",
        "sequence_name": "csm",
        "formatter_class": GenericBarcodeFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "CFR",
        "sequence_name": "csm",
        "formatter_class": GenericBarcodeFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "COS",
        "sequence_name": "csm",
        "formatter_class": GenericBarcodeFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "CPL",
        "sequence_name": "csm",
        "formatter_class": GenericBarcodeFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "PAM",
        "sequence_name": "pam",
        "formatter_class": GenericBarcodeFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "HT",
        "sequence_name": "ht",
        "formatter_class": GenericBarcodeFormatter,
        "enableChildrenCreation": False,
    },
]

for prefix_item in PREFIXES:
    for key in ["prefix", "sequence_name", "formatter_class"]:
        if not (key in prefix_item):
            raise KeyError("PREFIXES must all contain a prefix, sequence_name and formatter_class key.")
