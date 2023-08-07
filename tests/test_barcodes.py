from http import HTTPStatus
import json

# sequences
# starts at 2000000 for heron
# starts at 111111 for ht
# starts at 1 for sqp


def test_param_empty_prefix_value(client):
    response = client.post("/barcodes/new")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_invalid_prefix_is_rejected(client):
    response = client.post("/barcodes/TEST123412_edu/new")
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_get_new_barcode(client):
    response = client.post("/barcodes/SANG/new")
    assert response.json == {"barcode": "SANG-30D404"}
    assert response.status_code == HTTPStatus.CREATED


def test_get_new_barcode_for_ht(client):
    response = client.post("/barcodes/HT/new")
    assert response.json == {"barcode": "HT-111111"}
    assert response.status_code == HTTPStatus.CREATED


def test_get_new_barcode_for_sqp(client):
    response = client.post("/barcodes/SQPD/new")
    assert response.json == {"barcode": "SQPD-1-C"}
    assert response.status_code == HTTPStatus.CREATED


def test_get_new_barcode_with_text(client):
    response = client.post("/barcodes/SQPD/new?text=T12")
    assert response.json == {"barcode": "SQPD-T12-1-J"}
    assert response.status_code == HTTPStatus.CREATED


def test_get_new_barcode_with_wrong_text(client):
    response = client.post("/barcodes/SQPD/new?text=T120")
    assert response.json == {"errors": ["InvalidTextError"]}
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


def test_get_new_barcodes_group_as_url_param(client):
    response = client.post("/barcodes_group/SANG/new?count=3")
    resp = response.json
    resp["barcodes_group"]["barcodes"].sort()
    assert resp == {"barcodes_group": {"barcodes": ["SANG-30D404", "SANG-30D413", "SANG-30D422"], "id": 1}}
    assert response.status_code == HTTPStatus.CREATED


def test_get_new_barcodes_group_without_count(client):
    response = client.post("/barcodes_group/SANG/new")
    # 422 is returned on InvalidCountError
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_get_new_barcodes_group_with_wrong_value_count(client):
    response = client.post("/barcodes_group/SANG/new?count=WRONG")
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


def test_get_new_barcodes_group_with_wrong_value_negative(client):
    response = client.post("/barcodes_group/SANG/new?count=-124")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_get_new_barcodes_group_with_wrong_count(client):
    # The code now checks if post data is available and returns 422 rather than 500.
    response = client.post(
        "/barcodes_group/SANG/new", data=json.dumps({}), headers={"Content-Type": "application/json"}
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_get_new_barcodes_group_as_json_param(client):
    response = client.post(
        "/barcodes_group/SANG/new", data=json.dumps({"count": 2}), headers={"Content-Type": "application/json"}
    )
    resp = response.json
    resp["barcodes_group"]["barcodes"].sort()
    assert resp == {"barcodes_group": {"barcodes": ["SANG-30D404", "SANG-30D413"], "id": 1}}
    assert response.status_code == HTTPStatus.CREATED


def test_get_last_barcode(client):
    # with no barcode present
    response = client.get("/barcodes/SANG/last")
    assert response.status_code == HTTPStatus.NOT_FOUND

    # when creating barcodes
    response = client.post("/barcodes/SANG/new")
    response = client.get("/barcodes/SANG/last")
    assert response.json == {"barcode": "SANG-30D404"}
    assert response.status_code == HTTPStatus.OK
