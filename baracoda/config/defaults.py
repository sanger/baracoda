from os import getenv
from typing import List, Dict, Any

FLASK_APP = "baracoda"
FLASK_ENV = "development"
DB_DBNAME = "baracoda_dev"
DB_HOST = "localhost"
DB_PASSWORD = "postgres"
DB_PORT = "5432"
DB_USER = "postgres"
SEQUENCE_NAME = "heron"
SEQUENCE_START = "200000"
SLACK_API_TOKEN = "xoxb-123"
SLACK_CHANNEL_ID = "Cxxx"
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:postgres@localhost:5432/baracoda_dev"
X_DOMAINS = "*"

PREFIXES: List[Dict[str, Any]] = [
    {"prefix": "PHEC", "sequence_name": "heron", "convert": True},
    {"prefix": "PHWC", "sequence_name": "heron", "convert": True},
    {"prefix": "GCVR", "sequence_name": "heron", "convert": True},
    {"prefix": "SANG", "sequence_name": "heron", "convert": True},
    {"prefix": "BIRM", "sequence_name": "heron", "convert": True},
    {"prefix": "CAMB", "sequence_name": "heron", "convert": True},
    {"prefix": "EDIN", "sequence_name": "heron", "convert": True},
    {"prefix": "LIVE", "sequence_name": "heron", "convert": True},
    {"prefix": "OXON", "sequence_name": "heron", "convert": True},
    {"prefix": "SHEF", "sequence_name": "heron", "convert": True},
    {"prefix": "LOND", "sequence_name": "heron", "convert": True},
    {"prefix": "NORW", "sequence_name": "heron", "convert": True},
    {"prefix": "NIRE", "sequence_name": "heron", "convert": True},
    {"prefix": "BRIS", "sequence_name": "heron", "convert": True},
    {"prefix": "NOTT", "sequence_name": "heron", "convert": True},
    {"prefix": "EXET", "sequence_name": "heron", "convert": True},
    {"prefix": "NORT", "sequence_name": "heron", "convert": True},
    {"prefix": "LEED", "sequence_name": "heron", "convert": True},
    {"prefix": "PORT", "sequence_name": "heron", "convert": True},
    {"prefix": "MILK", "sequence_name": "heron", "convert": True},
    {"prefix": "BRIG", "sequence_name": "heron", "convert": True},
    {"prefix": "ALDP", "sequence_name": "heron", "convert": True},
    {"prefix": "TBSD", "sequence_name": "heron", "convert": True},
    {"prefix": "BHRT", "sequence_name": "heron", "convert": True},
    {"prefix": "LCST", "sequence_name": "heron", "convert": True},
    {"prefix": "CWAR", "sequence_name": "heron", "convert": True},
    {"prefix": "GLOU", "sequence_name": "heron", "convert": True},
    {"prefix": "PRIN", "sequence_name": "heron", "convert": True},
    {"prefix": "MTUN", "sequence_name": "heron", "convert": True},
    {"prefix": "HECH", "sequence_name": "heron", "convert": True},
    {"prefix": "WSFT", "sequence_name": "heron", "convert": True},
    {"prefix": "NWGH", "sequence_name": "heron", "convert": True},
    {"prefix": "EKHU", "sequence_name": "heron", "convert": True},
    {"prefix": "RSCH", "sequence_name": "heron", "convert": True},
    {"prefix": "GSTT", "sequence_name": "heron", "convert": True},
    {"prefix": "KGHT", "sequence_name": "heron", "convert": True},
    {"prefix": "WAHH", "sequence_name": "heron", "convert": True},
    {"prefix": "PAHT", "sequence_name": "heron", "convert": True},
    {"prefix": "TFCI", "sequence_name": "heron", "convert": True},
    {"prefix": "CAMC", "sequence_name": "heron", "convert": True},
    {"prefix": "QEUH", "sequence_name": "heron", "convert": True},
    {"prefix": "HT", "sequence_name": "ht", "convert": False},
    ]

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
    "X_DOMAINS",
    "PREFIXES"
)

for config in REQUIRED_CONFIG:
    if not eval(config):
        raise ValueError(f"{config} required for Flask application")

for prefix_item in PREFIXES:
    for key in ['prefix', 'sequence_name', 'convert']:
        if not(key in prefix_item):
            raise KeyError("PREFIXES must all contain a prefix, sequence_name and convert key.")
