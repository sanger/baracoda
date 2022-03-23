from typing import Any, Dict, List

from baracoda.formats import HeronCogUkIdFormatter, HeronPlateCherrypickedFormatter, SequencescapePlateBarcodeFormatter

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
PREFIXES: List[Dict[str, Any]] = [
    {"prefix": "ALDP", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "BHRT", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "BIRM", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "BRBR", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "BRIG", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "BRIS", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "CAMB", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "CAMC", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "CPTD", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "CWAR", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "EDIN", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "EKHU", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "EXET", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "GCVR", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "GLOU", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "GSTT", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "HECH", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "HSLL", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "KGHT", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "LCST", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "LEED", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "LIVE", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "LOND", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "LSPA", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "MILK", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "MTUN", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "NEWC", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "NIRE", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "NORT", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "NORW", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "NOTT", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "NWGH", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "OXON", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "PAHT", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "PHEC", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "PHWC", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "PLYM", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "PORT", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "PRIN", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "QEUH", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "RAND", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "RSCH", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "SANG", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "SHEF", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "TBSD", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "TFCI", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "WAHH", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "WSFT", "sequence_name": "heron", "formatter_class": HeronCogUkIdFormatter},
    {"prefix": "HT", "sequence_name": "ht", "formatter_class": HeronPlateCherrypickedFormatter},
    {"prefix": "DN", "sequence_name": "SEQ_DNAPLATE", "formatter_class": SequencescapePlateBarcodeFormatter},
]

for prefix_item in PREFIXES:
    for key in ["prefix", "sequence_name", "formatter_class"]:
        if not (key in prefix_item):
            raise KeyError("PREFIXES must all contain a prefix, sequence_name and formatter_class key.")
