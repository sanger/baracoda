from os import getenv

DB_HOST = getenv("DB_HOST")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_PORT = getenv("DB_PORT")
DB_USER = getenv("DB_USER")
SEQUENCE_NAME = getenv("SEQUENCE_NAME")
SEQUENCE_START = getenv("SEQUENCE_START")
SLACK_API_TOKEN = getenv("SLACK_API_TOKEN")

REQUIRED_CONFIG = (
    "DB_HOST",
    "DB_PASSWORD",
    "DB_PORT",
    "DB_USER",
    "SEQUENCE_NAME",
    "SEQUENCE_START",
    "SLACK_API_TOKEN",
)

for config in REQUIRED_CONFIG:
    if not eval(config):
        raise ValueError(f"{config} required for Flask application")
