from os import getenv
from typing import List, Dict

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

PREFIXES: List[Dict[str, str]] = [
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
    {"prefix": "HT", "sequence_name": "ht", "convert": False}]
