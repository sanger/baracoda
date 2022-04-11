import pytest

from baracoda.exceptions import InvalidPrefixError
from baracoda.helpers import get_prefix_item
from baracoda.operations import BarcodeOperations, ChildBarcodeOperations


# BarcodeOperations


def test_correct_prefix_obj_is_created(app, prefixes):
    with app.app_context():
        barcode_operations = BarcodeOperations(prefix="LEED")
        assert barcode_operations.prefix_item == get_prefix_item("LEED")


def test_sequence_is_correct_for_centres(app):
    with app.app_context():
        barcode_operations = BarcodeOperations(prefix="LEED")
        assert barcode_operations.sequence_name == "heron"


def test_sequence_is_correct_for_ht_plates(app):
    with app.app_context():
        barcode_operations = BarcodeOperations(prefix="HT")
        assert barcode_operations.sequence_name == "ht"


def test_sequence_is_correct_for_SQPD_plates(app):
    with app.app_context():
        barcode_operations = BarcodeOperations(prefix="SQPD")
        assert barcode_operations.sequence_name == "sqp"


def test_error_is_raised_if_prefix_is_not_valid(app):
    with app.app_context():
        with pytest.raises(InvalidPrefixError):
            _ = BarcodeOperations(prefix="MOON")


# ChildBarcodeOperations


def test_child_barcodes_are_created_when_new_barcode(app):
    with app.app_context():
        expected_child_barcodes = ["test-1"]
        assert ChildBarcodeOperations.create_child_barcodes("test", 1) == expected_child_barcodes


def test_child_barcodes_are_created_when_existing_barcode(app):
    with app.app_context():
        # Create a barcode record in the database
        ChildBarcodeOperations.create_child_barcodes("test", 5)
        # Expect child barcode to have correct when suffix when same barcode is used
        expected_child_barcodes = ["test-6"]
        assert ChildBarcodeOperations.create_child_barcodes("test", 1) == expected_child_barcodes


def test_correct_number_of_child_barcodes_are_created(app):
    with app.app_context():
        expected_child_barcodes = ["test-1", "test-2", "test-3"]
        assert ChildBarcodeOperations.create_child_barcodes("test", 3) == expected_child_barcodes
