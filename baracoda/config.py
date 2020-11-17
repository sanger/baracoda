from os import getenv

DB_DBNAME = getenv("DB_DBNAME")
DB_HOST = getenv("DB_HOST")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_PORT = getenv("DB_PORT")
DB_USER = getenv("DB_USER")
SEQUENCE_NAME = getenv("SEQUENCE_NAME")
SEQUENCE_START = getenv("SEQUENCE_START")
SLACK_API_TOKEN = getenv("SLACK_API_TOKEN", "")
SLACK_CHANNEL_ID = getenv("SLACK_CHANNEL_ID", "")
SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI", "")

REQUIRED_CONFIG = (
    "DB_DBNAME",
    "DB_HOST",
    "DB_PASSWORD",
    "DB_PORT",
    "DB_USER",
    "SEQUENCE_NAME",
    "SEQUENCE_START",
    "SLACK_API_TOKEN",
    "SLACK_CHANNEL_ID",
    "SQLALCHEMY_DATABASE_URI",
)

for config in REQUIRED_CONFIG:
    if not eval(config):
        raise ValueError(f"{config} required for Flask application")

PREFIXES: List[Dict[str, str]] = [{"prefix": "PHEC", "sequence_name": "heron"},
{"prefix": "PHWC", "sequence_name": "heron"},
{"prefix": "GCVR", "sequence_name": "heron"},
{"prefix": "SANG", "sequence_name": "heron"},
{"prefix": "BIRM", "sequence_name": "heron"},
{"prefix": "CAMB", "sequence_name": "heron"},
{"prefix": "EDIN", "sequence_name": "heron"},
{"prefix": "LIVE", "sequence_name": "heron"},
{"prefix": "OXON", "sequence_name": "heron"},
{"prefix": "SHEF", "sequence_name": "heron"},
{"prefix": "LOND", "sequence_name": "heron"},
{"prefix": "NORW", "sequence_name": "heron"},
{"prefix": "NIRE", "sequence_name": "heron"},
{"prefix": "BRIS", "sequence_name": "heron"},
{"prefix": "NOTT", "sequence_name": "heron"},
{"prefix": "EXET", "sequence_name": "heron"},
{"prefix": "NORT", "sequence_name": "heron"},
{"prefix": "LEED", "sequence_name": "heron"},
{"prefix": "PORT", "sequence_name": "heron"},
{"prefix": "MILK", "sequence_name": "heron"},
{"prefix": "BRIG", "sequence_name": "heron"},
{"prefix": "ALDP", "sequence_name": "heron"},
{"prefix": "TBSD", "sequence_name": "heron"},
{"prefix": "BHRT", "sequence_name": "heron"},
{"prefix": "LCST", "sequence_name": "heron"},
{"prefix": "CWAR", "sequence_name": "heron"},
{"prefix": "GLOU", "sequence_name": "heron"},
{"prefix": "PRIN", "sequence_name": "heron"},
{"prefix": "MTUN", "sequence_name": "heron"},
{"prefix": "HECH", "sequence_name": "heron"},
{"prefix": "WSFT", "sequence_name": "heron"},
{"prefix": "NWGH", "sequence_name": "heron"},
{"prefix": "EKHU", "sequence_name": "heron"},
{"prefix": "RSCH", "sequence_name": "heron"},
{"prefix": "GSTT", "sequence_name": "heron"},
{"prefix": "KGHT", "sequence_name": "heron"},
{"prefix": "WAHH", "sequence_name": "heron"},
{"prefix": "PAHT", "sequence_name": "heron"},
{"prefix": "TFCI", "sequence_name": "heron"},
{"prefix": "CAMC", "sequence_name": "heron"},
{"prefix": "QEUH", "sequence_name": "heron"},
{"prefix": "HT", "sequence_name": "ht"}]
