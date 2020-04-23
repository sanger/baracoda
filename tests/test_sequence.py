import json


def test_param_empty_prefix_value(client):
    response = client.post(
        "/barcodes//new", headers={"Content-type": "application/json"}
    )
    assert response.status_code == 404


def test_invalid_prefix_is_forbidden(client):
    response = client.post(
        "/barcodes/TEST/new", headers={"Content-type": "application/json"}
    )
    assert response.status_code == 403


def test_get_new_barcode(client):
    response = client.post(
        "/barcodes/SANG/new", headers={"Content-type": "application/json"}
    )
    assert response.json == {"barcode": "SANG-30D404"}
    assert response.status_code == 201


def test_get_last_barcode(client):
    response = client.get(
        "/barcodes/SANG/last", headers={"Content-type": "application/json"}
    )
    assert response.json == {"barcode": "SANG-30D404"}
    assert response.status_code == 200


def test_get_index_prefixes(client, app):
    response = client.get("/prefixes", headers={"Content-type": "application/json"})
    assert response.json == [
        {
            "prefix": "SANG",
            "description": "Sanger barcodes",
            "centre": "Sanger Institute",
        },
        {"prefix": "NIRE", "description": "Nire barcodes", "centre": "Nire"},
    ]
    assert response.status_code == 200


def test_prefix_search(client):
    response = client.get(
        "/search/prefixes?centre=Sanger Institute",
        headers={"Content-type": "application/json"},
    )
    assert response.json == [
        {
            "prefix": "SANG",
            "description": "Sanger barcodes",
            "centre": "Sanger Institute",
        }
    ]
    assert response.status_code == 200


def test_wrong_argument(client):
    response = client.get(
        "/search/prefixes?asdf=Sanger", headers={"Content-type": "application/json"}
    )
    assert response.status_code == 422
