from http import HTTPStatus
import json
import pytest

CHILD_BARCODE_PREFIXES = ["SQPD"]


@pytest.mark.parametrize("prefix", CHILD_BARCODE_PREFIXES)
def test_new_child_barcode_can_create_single_barcode(client, prefix, enable_children_for_prefix):
    response = client.post(
        f"/child-barcodes/{ prefix }/new",
        data=json.dumps({"barcode": f"{ prefix }-1"}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"id": 1, "barcodes": [f"{ prefix }-1-1"]}}
    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.parametrize("prefix", CHILD_BARCODE_PREFIXES)
def test_new_child_barcode_can_create_several_barcodes(client, prefix, enable_children_for_prefix):
    response = client.post(
        f"/child-barcodes/{ prefix }/new",
        data=json.dumps({"barcode": f"{ prefix }-1", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {
        "barcodes_group": {"id": 1, "barcodes": [f"{ prefix }-1-1", f"{ prefix }-1-2", f"{ prefix }-1-3"]}
    }
    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.parametrize("prefix", CHILD_BARCODE_PREFIXES)
def test_new_child_barcode_different_parent_keep_their_own_counting_of_children(
    client, prefix, enable_children_for_prefix
):
    # Parent 1
    response = client.post(
        f"/child-barcodes/{ prefix }/new",
        data=json.dumps({"barcode": f"{ prefix }-1", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {
        "barcodes_group": {"id": 1, "barcodes": [f"{ prefix }-1-1", f"{ prefix }-1-2", f"{ prefix }-1-3"]}
    }
    assert response.status_code == HTTPStatus.CREATED

    # Parent 2
    response = client.post(
        f"/child-barcodes/{ prefix }/new",
        data=json.dumps({"barcode": f"{ prefix }-2", "count": 2}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"id": 2, "barcodes": [f"{ prefix }-2-1", f"{ prefix }-2-2"]}}
    assert response.status_code == HTTPStatus.CREATED

    # Parent 1 again
    response = client.post(
        f"/child-barcodes/{ prefix }/new",
        data=json.dumps({"barcode": f"{ prefix }-1", "count": 1}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"id": 3, "barcodes": [f"{ prefix }-1-4"]}}
    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.parametrize("prefix", CHILD_BARCODE_PREFIXES)
def test_new_child_barcode_incorrect_valid_prefixed_parent_can_create_unattributed_children(
    client, prefix, enable_children_for_prefix
):
    response = client.post(
        f"/child-barcodes/{ prefix }/new",
        data=json.dumps({"barcode": "SANG-1", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {
        "barcodes_group": {"id": 1, "barcodes": [f"{ prefix }-1", f"{ prefix }-2", f"{ prefix }-3"]}
    }
    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.parametrize("prefix", CHILD_BARCODE_PREFIXES)
def test_new_child_barcode_invalid_prefixed_parent_can_create_unattributed_children(
    client, prefix, enable_children_for_prefix
):
    response = client.post(
        f"/child-barcodes/{ prefix }/new",
        data=json.dumps({"barcode": "test-123", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {
        "barcodes_group": {"barcodes": [f"{ prefix }-1", f"{ prefix }-2", f"{ prefix }-3"], "id": 1}
    }
    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.parametrize("prefix", CHILD_BARCODE_PREFIXES)
def test_new_child_barcode_valid_parent_can_create_attributed_children_and_descendants_can_continue_lineage(
    client, prefix, enable_children_for_prefix
):
    response = client.post(
        f"/child-barcodes/{ prefix }/new",
        data=json.dumps({"barcode": f"{ prefix }-1", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {
        "barcodes_group": {"barcodes": [f"{ prefix }-1-1", f"{ prefix }-1-2", f"{ prefix }-1-3"], "id": 1}
    }
    assert response.status_code == HTTPStatus.CREATED

    response = client.post(
        f"/child-barcodes/{ prefix }/new",
        data=json.dumps({"barcode": f"{ prefix }-1-1", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {
        "barcodes_group": {"barcodes": [f"{ prefix }-1-4", f"{ prefix }-1-5", f"{ prefix }-1-6"], "id": 2}
    }
    assert response.status_code == HTTPStatus.CREATED

    response = client.post(
        f"/child-barcodes/{ prefix }/new",
        data=json.dumps({"barcode": f"{ prefix }-1-5", "count": 1}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"barcodes": [f"{ prefix }-1-7"], "id": 3}}
    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.parametrize("prefix", CHILD_BARCODE_PREFIXES)
def test_new_child_barcode_valid_parent_can_create_attributed_children_and_children_and_parent_can_continue_lineage(
    client, prefix
):
    # Parent
    response = client.post(
        f"/child-barcodes/{ prefix }/new",
        data=json.dumps({"barcode": f"{ prefix }-1", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {
        "barcodes_group": {"barcodes": [f"{ prefix }-1-1", f"{ prefix }-1-2", f"{ prefix }-1-3"], "id": 1}
    }
    assert response.status_code == HTTPStatus.CREATED

    # Children 1
    response = client.post(
        f"/child-barcodes/{ prefix }/new",
        data=json.dumps({"barcode": f"{ prefix }-1-1", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {
        "barcodes_group": {"barcodes": [f"{ prefix }-1-4", f"{ prefix }-1-5", f"{ prefix }-1-6"], "id": 2}
    }
    assert response.status_code == HTTPStatus.CREATED

    # Children 2
    response = client.post(
        f"/child-barcodes/{ prefix }/new",
        data=json.dumps({"barcode": f"{ prefix }-1-2", "count": 2}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"barcodes": [f"{ prefix }-1-7", f"{ prefix }-1-8"], "id": 3}}
    assert response.status_code == HTTPStatus.CREATED

    # Parent again
    response = client.post(
        f"/child-barcodes/{ prefix }/new",
        data=json.dumps({"barcode": f"{ prefix }-1", "count": 2}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"barcodes": [f"{ prefix }-1-9", f"{ prefix }-1-10"], "id": 4}}
    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.parametrize("prefix", CHILD_BARCODE_PREFIXES)
def test_new_child_barcode_invalid_parent_can_create_unattributed_children(client, prefix, enable_children_for_prefix):
    response = client.post(
        f"/child-barcodes/{ prefix }/new",
        data=json.dumps({"barcode": f"{ prefix }1-1", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {
        "barcodes_group": {"barcodes": [f"{ prefix }-1", f"{ prefix }-2", f"{ prefix }-3"], "id": 1}
    }
    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.parametrize("prefix", CHILD_BARCODE_PREFIXES)
def test_new_child_barcode_invalid_parent_can_create_unattributed_children_several_times(
    client, prefix, enable_children_for_prefix
):
    response = client.post(
        f"/child-barcodes/{ prefix }/new",
        data=json.dumps({"barcode": f"{ prefix }1-1", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {
        "barcodes_group": {"barcodes": [f"{ prefix }-1", f"{ prefix }-2", f"{ prefix }-3"], "id": 1}
    }
    assert response.status_code == HTTPStatus.CREATED

    response = client.post(
        f"/child-barcodes/{ prefix }/new",
        data=json.dumps({"barcode": f"{ prefix }1-1", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {
        "barcodes_group": {"barcodes": [f"{ prefix }-4", f"{ prefix }-5", f"{ prefix }-6"], "id": 2}
    }
    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.parametrize("prefix", CHILD_BARCODE_PREFIXES)
def test_new_child_barcode_unattributed_children_of_invalid_parent_can_start_own_lineage(
    client, prefix, enable_children_for_prefix
):
    # invalid parent
    response = client.post(
        f"/child-barcodes/{ prefix }/new",
        data=json.dumps({"barcode": f"{ prefix }1-1", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {
        "barcodes_group": {"barcodes": [f"{ prefix }-1", f"{ prefix }-2", f"{ prefix }-3"], "id": 1}
    }
    assert response.status_code == HTTPStatus.CREATED

    # unattributed_children
    response = client.post(
        f"/child-barcodes/{ prefix }/new",
        data=json.dumps({"barcode": f"{ prefix }-1", "count": 2}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"barcodes": [f"{ prefix }-1-1", f"{ prefix }-1-2"], "id": 2}}
    assert response.status_code == HTTPStatus.CREATED

    # new lineage
    response = client.post(
        f"/child-barcodes/{ prefix }/new",
        data=json.dumps({"barcode": f"{ prefix }-1-2", "count": 2}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"barcodes": [f"{ prefix }-1-3", f"{ prefix }-1-4"], "id": 3}}
    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.parametrize("prefix", CHILD_BARCODE_PREFIXES)
def test_new_child_barcode_impostor_children_with_possible_parent_can_be_stopped(
    client, prefix, enable_children_for_prefix
):
    # invalid parent
    response = client.post(
        f"/child-barcodes/{ prefix }/new",
        data=json.dumps({"barcode": f"{ prefix }-1", "count": 2}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"barcodes": [f"{ prefix }-1-1", f"{ prefix }-1-2"], "id": 1}}
    assert response.status_code == HTTPStatus.CREATED

    # Hacking children
    response = client.post(
        f"/child-barcodes/{ prefix }/new",
        data=json.dumps({"barcode": f"{ prefix }-1-3", "count": 1}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"errors": ["InvalidParentBarcode"]}
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


@pytest.mark.parametrize("prefix", CHILD_BARCODE_PREFIXES)
def test_new_child_barcode_impostor_children_without_possible_parent_can_be_stopped(
    client, prefix, enable_children_for_prefix
):
    # Hacking children
    response = client.post(
        f"/child-barcodes/{ prefix }/new",
        data=json.dumps({"barcode": f"{ prefix }-1-3", "count": 1}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"errors": ["InvalidParentBarcode"]}
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


@pytest.mark.parametrize("prefix", CHILD_BARCODE_PREFIXES)
def test_new_child_barcode_children_of_invalid_parent_can_create_children(client, prefix, enable_children_for_prefix):
    response = client.post(
        f"/child-barcodes/{ prefix }/new",
        data=json.dumps({"barcode": f"{ prefix }1-1", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {
        "barcodes_group": {"barcodes": [f"{ prefix }-1", f"{ prefix }-2", f"{ prefix }-3"], "id": 1}
    }
    assert response.status_code == HTTPStatus.CREATED

    response = client.post(
        f"/child-barcodes/{ prefix }/new",
        data=json.dumps({"barcode": f"{ prefix }-1", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {
        "barcodes_group": {"barcodes": [f"{ prefix }-1-1", f"{ prefix }-1-2", f"{ prefix }-1-3"], "id": 2}
    }
    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.parametrize("prefix", CHILD_BARCODE_PREFIXES)
def test_new_child_barcode_with_unknown_prefix_rejects_request(client, prefix, enable_children_for_prefix):
    response = client.post(
        "/child-barcodes/unknown/new",
        data=json.dumps({"barcode": "SANG-1", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"errors": ["InvalidPrefixError"]}
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


@pytest.mark.parametrize("prefix", CHILD_BARCODE_PREFIXES)
def test_no_child_barcode(client, prefix, enable_children_for_prefix):
    response = client.post(
        "/child-barcodes/test/new", data=json.dumps({}), headers={"Content-Type": "application/json"}
    )
    assert response.json == {"errors": ["InvalidBarcodeError"]}
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("prefix", CHILD_BARCODE_PREFIXES)
def test_bad_child_barcode(client, prefix, enable_children_for_prefix):
    response = client.post(
        "/child-barcodes/test/new", data=json.dumps({"barcode": " "}), headers={"Content-Type": "application/json"}
    )
    assert response.json == {"errors": ["InvalidBarcodeError"]}
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("prefix", CHILD_BARCODE_PREFIXES)
def test_bad_count(client, prefix, enable_children_for_prefix):
    response = client.post(
        "/child-barcodes/test/new",
        data=json.dumps({"barcode": "test", "count": 0}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"errors": ["InvalidCountError"]}
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
