from baracoda.operations import BarcodeOperations
from baracoda.exceptions import InvalidPrefixError
import pytest

def test_sequence_is_correct_for_centres(app):
  with app.app_context():
    barcode_operations = BarcodeOperations(prefix="LEED")
    assert barcode_operations.sequence_name == "heron"

def test_sequence_is_correct_for_ht_plates(app):
  with app.app_context():
    barcode_operations = BarcodeOperations(prefix="HT")
    assert barcode_operations.sequence_name == "ht"

def test_error_is_raised_if_prefix_is_not_valid(app):
  with app.app_context():
    with pytest.raises(InvalidPrefixError):
      barcode_operations = BarcodeOperations(prefix="MOON")