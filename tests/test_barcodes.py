from http import HTTPStatus
import json
import logging

logger = logging.getLogger(__name__)

# sequences
# starts at 2000000 for heron
# starts at 111111 for ht
# starts at 1 for sqp


def test_param_empty_prefix_value(client):
    response = client.post("/barcodes/new")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_invalid_prefix_is_rejected(client, caplog):
    response = client.post("/barcodes/TEST123412_edu/new", headers={"Content-Type": "application/json"})
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "InvalidPrefixError: Invalid prefix for Heron barcode TEST123412_edu" in caplog.text


def test_get_new_barcode(client):
    response = client.post("/barcodes/SANG/new", headers={"Content-Type": "application/json"})
    assert response.json == {"barcode": "SANG-30D404"}
    assert response.status_code == HTTPStatus.CREATED


def test_get_new_barcode_for_ht(client):
    response = client.post("/barcodes/HT/new", headers={"Content-Type": "application/json"})
    assert response.json == {"barcode": "HT-111111"}
    assert response.status_code == HTTPStatus.CREATED


def test_get_new_barcode_for_sqp(client):
    response = client.post("/barcodes/SQPD/new", headers={"Content-Type": "application/json"})
    assert response.json == {"barcode": "SQPD-1-C"}
    assert response.status_code == HTTPStatus.CREATED


def test_get_new_barcode_for_rvi(client):
    response = client.post("/barcodes/RVI/new", headers={"Content-Type": "application/json"})
    assert response.json == {"barcode": "RVI-111111"}
    assert response.status_code == HTTPStatus.CREATED


def test_get_new_barcode_with_text(client):
    response = client.post("/barcodes/SQPD/new?text=T12", headers={"Content-Type": "application/json"})
    assert response.json == {"barcode": "SQPD-T12-1-J"}
    assert response.status_code == HTTPStatus.CREATED


def test_get_new_barcode_with_wrong_text(client, caplog):
    response = client.post("/barcodes/SQPD/new?text=T120", headers={"Content-Type": "application/json"})
    assert response.json == {"errors": ["InvalidTextError"]}
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert "InvalidTextError: Please add the 'text' param to the request" in caplog.text


def test_get_new_barcodes_group_as_url_param(client):
    response = client.post("/barcodes_group/SANG/new?count=3", headers={"Content-Type": "application/json"})
    resp = response.json
    resp["barcodes_group"]["barcodes"].sort()
    assert resp == {"barcodes_group": {"barcodes": ["SANG-30D404", "SANG-30D413", "SANG-30D422"], "id": 1}}
    assert response.status_code == HTTPStatus.CREATED


def test_get_new_barcodes_group_without_count(client, caplog):
    response = client.post("/barcodes_group/SANG/new", headers={"Content-Type": "application/json"})
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "Bad Request: The browser (or proxy) sent a request that this server could not understand" in caplog.text


def test_get_new_barcodes_group_with_wrong_value_count(client, caplog):
    response = client.post("/barcodes_group/SANG/new?count=WRONG")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "InvalidCountError: Count value is not a positive integer" in caplog.text


def test_get_new_barcodes_group_with_wrong_value_negative(client, caplog):
    response = client.post("/barcodes_group/SANG/new?count=-124", headers={"Content-Type": "application/json"})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "InvalidCountError: Count value is not a positive integer" in caplog.text


def test_get_new_barcodes_group_with_wrong_count(client, caplog):
    # Since the count is no longer a param the get_count_param method looks at the json body
    # this response.json method will internal error unless we pass the correct headers and data
    response = client.post(
        "/barcodes_group/SANG/new", data=json.dumps({}), headers={"Content-Type": "application/json"}
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "InvalidCountError: Please add the 'count' param to the request" in caplog.text


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
    response = client.post("/barcodes/SANG/new", headers={"Content-Type": "application/json"})
    response = client.get("/barcodes/SANG/last")
    assert response.json == {"barcode": "SANG-30D404"}
    assert response.status_code == HTTPStatus.OK
