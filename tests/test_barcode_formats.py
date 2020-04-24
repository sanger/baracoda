from baracoda.barcode_formats import HeronFormatter


def test_checksum_conversion():
    params = {"prefix": "SANG"}
    formatter = HeronFormatter(params)
    assert formatter.checksum("4A99") == "6"
    assert formatter.checksum("102B1") == "B"


def test_checksum_when_sum_mod_16_is_0():
    params = {"prefix": "SANG"}
    formatter = HeronFormatter(params)
    assert formatter.checksum("1812") == "0"


def test_checksum_when_sum_mod_16_is_not_0():
    params = {"prefix": "SANG"}
    formatter = HeronFormatter(params)
    assert formatter.checksum("1813") == "F"


def test_barcode_example_1():
    params = {"prefix": "SANG"}
    formatter = HeronFormatter(params)
    assert formatter.barcode("4A99") == "SANG-4A996"


def test_barcode_example_2():
    params = {"prefix": "NIRE"}
    formatter = HeronFormatter(params)
    assert formatter.barcode("102B1") == "NIRE-102B1B"


def barcode_for(barcode: str):
    prefix, number_and_checksum = barcode.split("-")
    number = number_and_checksum[:-1]
    formatter = HeronFormatter({"prefix": prefix})
    return formatter.barcode(number)


def test_several_barcodes():
    test_barcodes = [
        "LOND-DE672",
        "LOND-DFFEF",
        "LOND-D54DB",
        "LOND-D7AAA",
        "LOND-E5924",
        "LOND-E4BF2",
        "LOND-E2453",
        "LOND-E4521",
        "LOND-D4D77",
        "LOND-E5D64",
        "LOND-E007F",
        "LOND-DBE6E",
        "LOND-D999C",
        "LOND-D37E3",
        "LOND-E2259",
        "LOND-E458B",
        "LOND-D6504",
        "LOND-E5EE9",
        "LOND-DD28E",
        "LOND-DB47B",
    ]
    obtained_barcodes = []
    for barcode in test_barcodes:
        obtained_barcodes.append(barcode_for(barcode))

    assert obtained_barcodes == test_barcodes
