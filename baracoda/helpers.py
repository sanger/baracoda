import logging

logger = logging.getLogger(__name__)

from flask import current_app

def get_prefix_item(prefix: str):
  """
    Method which returns prefix object.
    This will contain the prefix, the sequence and whether any barcode for that prefix needs
    toi be formatted.

    Arguments:
        value {str} -- the actual prefix

    Returns:
        str -- prefix object e.g. { "prefix": "abc", "sequence_name": "seq", "convert": False}
    """
  return next((item for item in current_app.config["PREFIXES"] if item["prefix"] == prefix), None)