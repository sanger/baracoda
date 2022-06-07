import pytest
from baracoda.exceptions import UnsupportedEncodingForPrefix, InvalidBarcodeError, InvalidCountError, UnsupportedChildrenCreation, UnsupportedChildrenCreation, InvalidPrefixError, InvalidCountError, InvalidBarcodeError

EXCEPTIONS = [
    UnsupportedEncodingForPrefix,
    UnsupportedChildrenCreation,
    InvalidPrefixError,
    InvalidCountError,
    InvalidBarcodeError
]

@pytest.mark.parametrize("exception_class", EXCEPTIONS)
def test_exception_str(exception_class):
    msg = 'testing message'
    assert msg in str(exception_class(msg))
