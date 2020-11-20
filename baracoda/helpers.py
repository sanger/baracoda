import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

from flask import current_app

def get_prefix_item(prefix: str) -> Optional[Dict]:
  """
    Method which returns prefix object.
    This will contain the prefix, the sequence and whether any barcode for that prefix needs
    to be formatted.

    Arguments:
        value {str} -- the actual prefix

    Returns:
        Dict -- prefix object e.g. { "prefix": "abc", "sequence_name": "seq", "convert": False} or
        None -- if the prefix item is not available
    """
  return next((item for item in current_app.config["PREFIXES"] if item["prefix"] == prefix), None)