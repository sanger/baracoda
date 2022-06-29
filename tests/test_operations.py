import pytest

from baracoda.exceptions import InvalidPrefixError
from baracoda.helpers import get_prefix_item
from baracoda.operations import BarcodeOperations, InvalidParentBarcode


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


# Child barcode operations


def test_child_barcodes_are_created_when_new_barcode(app):
    with app.app_context():
        barcode_operations = BarcodeOperations(prefix="SQPD")
        expected_child_barcodes = ["SQPD-1-C"]
        assert barcode_operations.create_child_barcodes("SQPD", 1) == expected_child_barcodes


def test_child_barcodes_are_created_when_existing_barcode(app):
    with app.app_context():
        # Create a barcode record in the database
        barcode_operations = BarcodeOperations(prefix="SQPD")
        barcode_operations.create_child_barcodes("SQPD", 5)
        # Expect child barcode to have correct when suffix when same barcode is used
        expected_child_barcodes = ["SQPD-6-H"]
        assert barcode_operations.create_child_barcodes("SQPD", 1) == expected_child_barcodes


def test_correct_number_of_child_barcodes_are_created(app):
    with app.app_context():
        barcode_operations = BarcodeOperations(prefix="SQPD")
        expected_child_barcodes = ["SQPD-1-C", "SQPD-2-D", "SQPD-3-E"]
        assert barcode_operations.create_child_barcodes("SQPD", 3) == expected_child_barcodes


def test_is_valid_parent_barcode(app):
    with app.app_context():
        barcode_operations = BarcodeOperations(prefix="HT")
        assert barcode_operations.is_valid_parent_barcode("HT-1234") is True
        assert barcode_operations.is_valid_parent_barcode("SQPD-1234") is False
        assert barcode_operations.is_valid_parent_barcode("HT-1234-1") is True
        assert barcode_operations.is_valid_parent_barcode("HT-1234-1-1") is False
        assert barcode_operations.is_valid_parent_barcode("HT-1234-1-1-1") is False
        assert barcode_operations.is_valid_parent_barcode("HT1234") is False
        assert barcode_operations.is_valid_parent_barcode("HT") is False
        assert barcode_operations.is_valid_parent_barcode("HT-") is False
        assert barcode_operations.is_valid_parent_barcode("") is False


def test_validate_barcode_parent_information(app):
    with app.app_context():
        barcode_operations = BarcodeOperations(prefix="SQPD")
        with pytest.raises(InvalidParentBarcode):
            barcode_operations.validate_barcode_parent_information(
                {"parent_barcode": "SQPD-1", "child": "1", "suffix": "A"}
            )


def test_extract_barcode_parent_information(app):
    with app.app_context():
        barcode_operations = BarcodeOperations(prefix="SQPD")

        assert barcode_operations.extract_barcode_parent_information("SQPD-1") == {
            "parent_barcode": "SQPD-1",
            "child": None,
            "suffix": None,
        }

        assert barcode_operations.extract_barcode_parent_information("SQPD-1-C") == {
            "parent_barcode": "SQPD-1",
            "child": None,
            "suffix": "C",
        }

        assert barcode_operations.extract_barcode_parent_information("SQPD-11-22") == {
            "parent_barcode": "SQPD-11",
            "child": "22",
            "suffix": None,
        }

        assert barcode_operations.extract_barcode_parent_information("SQPD-234-56-Z") == {
            "parent_barcode": "SQPD-234",
            "child": "56",
            "suffix": "Z",
        }

        assert barcode_operations.extract_barcode_parent_information("SQPD-11-22-33") is None

        assert barcode_operations.extract_barcode_parent_information("DN-11-22") is None
