import pytest
from baracoda.exceptions import (
    UnsupportedEncodingForPrefix,
    UnsupportedChildrenCreation,
    InvalidPrefixError,
    InvalidCountError,
    InvalidBarcodeError,
    UnsupportedTextCodeValue,
)

EXCEPTIONS = [
    UnsupportedEncodingForPrefix,
    UnsupportedChildrenCreation,
    InvalidPrefixError,
    InvalidCountError,
    InvalidBarcodeError,
    UnsupportedTextCodeValue,
]


@pytest.mark.parametrize("exception_class", EXCEPTIONS)
def test_exception_str(exception_class):
    msg = "testing message"
    assert msg in str(exception_class(msg))
    assert len(str(exception_class())) > 0
