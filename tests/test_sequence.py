import json


def test_param_empty_prefix_value(client):
    response = client.post(
        "/barcodes//new", headers={"Content-type": "application/json"}
    )
    assert response.status_code == 404


def test_invalid_prefix_is_rejected(client):
    response = client.post(
        "/barcodes/TEST123412_edu/new", headers={"Content-type": "application/json"}
    )
    assert response.status_code == 422


def test_get_new_barcode(client):
    response = client.post(
        "/barcodes/SANG/new", headers={"Content-type": "application/json"}
    )
    assert response.json == {"barcode": "SANG-30D404"}
    assert response.status_code == 201


def test_get_new_count_barcodes(client):
    response = client.post(
        "/barcodes/SANG/new",
        headers={"Content-type": "application/json"},
        data=json.dumps({"count": 10}),
    )
    assert len(response.json) == 10
    assert response.status_code == 201


def test_get_last_barcode(client):
    response = client.post(
        "/barcodes/SANG/new", headers={"Content-type": "application/json"}
    )
    response = client.get(
        "/barcodes/SANG/last", headers={"Content-type": "application/json"}
    )
    assert response.json == {"barcode": "SANG-30D404"}
    assert response.status_code == 200
