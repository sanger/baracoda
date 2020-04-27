from http import HTTPStatus


def test_param_empty_prefix_value(client):
    response = client.post("/barcodes/new")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_invalid_prefix_is_rejected(client):
    response = client.post("/barcodes/TEST123412_edu/new")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_get_new_barcode(client):
    response = client.post("/barcodes/SANG/new")
    assert response.json == {"barcode": "SANG-30D404"}
    assert response.status_code == HTTPStatus.CREATED


def test_get_last_barcode(client):
    response = client.post("/barcodes/SANG/new")
    response = client.get("/barcodes/SANG/last")
    assert response.json == {"barcode": "SANG-30D404"}
    assert response.status_code == HTTPStatus.OK
