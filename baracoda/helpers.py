import logging

logger = logging.getLogger(__name__)

from flask import current_app

def get_prefix_item(prefix: str):
  return next((item for item in current_app.config["PREFIXES"] if item["prefix"] == prefix), None)