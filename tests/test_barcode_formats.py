from baracoda.barcode_formats import HeronFormatter
from pytest import raises
from baracoda.exceptions import WrongPrefixError

def check_invalidates_params(params):
    with raises(WrongPrefixError) as pytest_wrapped_e:
            HeronFormatter(params)
    assert pytest_wrapped_e.type == WrongPrefixError
    valid = HeronFormatter({'prefix': 'VALID'})
    assert valid.validate_params(params) == False

def test_invalid_when_empty_params():
    check_invalidates_params(None)
    check_invalidates_params({})
    check_invalidates_params({'prefix': None})

def test_invalid_when_incorrect_format():
    check_invalidates_params({'prefix': 'test'})
    check_invalidates_params({'prefix': 'TEST TEST'})
    check_invalidates_params({'prefix': 'TEST*TEST'})
    check_invalidates_params({'prefix': ' TEST '})
    check_invalidates_params({'prefix': 'TESTe'})
    
def test_invalid_when_length_incorrect():
    check_invalidates_params({'prefix': ''})
    check_invalidates_params({'prefix': 'ABCDEFGHIJKL'})

def test_validate_params_with_right_format():
    params = {'prefix': 'VALID'}
    valid = HeronFormatter(params)
    assert valid.validate_params(params) == True

def test_checksum_conversion():
    params = {'prefix': 'SANG'}
    formatter = HeronFormatter(params)
    assert formatter.checksum('4A99') == '6'
    assert formatter.checksum('102B1') == 'B'

def test_checksum_when_sum_mod_16_is_0():
    params = {'prefix': 'SANG'}
    formatter = HeronFormatter(params)
    assert formatter.checksum('1812') == '0'

def test_checksum_when_sum_mod_16_is_not_0():
    params = {'prefix': 'SANG'}
    formatter = HeronFormatter(params)
    assert formatter.checksum('1813') == 'F'

def test_barcode_example_1():
    params = {'prefix': 'SANG'}
    formatter = HeronFormatter(params)
    assert formatter.barcode('4A99') == 'SANG-4A996'

def test_barcode_example_2():
    params = {'prefix': 'NIRE'}
    formatter = HeronFormatter(params)
    assert formatter.barcode('102B1') == 'NIRE-102B1B'
