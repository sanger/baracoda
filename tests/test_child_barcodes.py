from http import HTTPStatus
import json

# sequences
# starts at 1 for sqp


def test_new_child_barcode(client):
    response = client.post(
        "/child-barcodes/new", data=json.dumps({"barcode": "test"}), headers={"Content-Type": "application/json"}
    )
    assert response.json == {"barcodes": ["test-1"]}
    assert response.status_code == HTTPStatus.CREATED


def test_new_child_barcode_with_count(client):
    response = client.post(
        "/child-barcodes/new",
        data=json.dumps({"barcode": "test", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes": ["test-1", "test-2", "test-3"]}
    assert response.status_code == HTTPStatus.CREATED


def test_no_child_barcode(client):
    response = client.post("/child-barcodes/new", data=json.dumps({}), headers={"Content-Type": "application/json"})
    assert response.json == {"errors": ["InvalidBarcodeError"]}
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_bad_child_barcode(client):
    response = client.post(
        "/child-barcodes/new", data=json.dumps({"barcode": " "}), headers={"Content-Type": "application/json"}
    )
    assert response.json == {"errors": ["InvalidBarcodeError"]}
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_bad_count(client):
    response = client.post(
        "/child-barcodes/new",
        data=json.dumps({"barcode": "test", "count": 0}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"errors": ["InvalidCountError"]}
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
