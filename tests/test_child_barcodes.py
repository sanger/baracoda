from http import HTTPStatus
import json

# sequences
# starts at 1 for sqp


def test_new_child_barcode_can_create_single_barcode(client):
    response = client.post(
        "/child-barcodes/HT/new", data=json.dumps({"barcode": "HT-1"}), headers={"Content-Type": "application/json"}
    )
    assert response.json == {"barcodes_group": {"id": 1, "barcodes": ["HT-1-1"]}}
    assert response.status_code == HTTPStatus.CREATED


def test_new_child_barcode_can_create_several_barcodes(client):
    response = client.post(
        "/child-barcodes/HT/new",
        data=json.dumps({"barcode": "HT-1", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"id": 1, "barcodes": ["HT-1-1", "HT-1-2", "HT-1-3"]}}
    assert response.status_code == HTTPStatus.CREATED


def test_new_child_barcode_different_parent_keep_their_own_counting_of_children(client):
    # Parent 1
    response = client.post(
        "/child-barcodes/HT/new",
        data=json.dumps({"barcode": "HT-1", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"id": 1, "barcodes": ["HT-1-1", "HT-1-2", "HT-1-3"]}}
    assert response.status_code == HTTPStatus.CREATED

    # Parent 2
    response = client.post(
        "/child-barcodes/HT/new",
        data=json.dumps({"barcode": "HT-2", "count": 2}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"id": 2, "barcodes": ["HT-2-1", "HT-2-2"]}}
    assert response.status_code == HTTPStatus.CREATED

    # Parent 1 again
    response = client.post(
        "/child-barcodes/HT/new",
        data=json.dumps({"barcode": "HT-1", "count": 1}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"id": 3, "barcodes": ["HT-1-4"]}}
    assert response.status_code == HTTPStatus.CREATED


def test_new_child_barcode_incorrect_valid_prefixed_parent_can_create_unattributed_children(client):
    response = client.post(
        "/child-barcodes/HT/new",
        data=json.dumps({"barcode": "SANG-1", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"id": 1, "barcodes": ["HT-111111", "HT-111112", "HT-111113"]}}
    assert response.status_code == HTTPStatus.CREATED


def test_new_child_barcode_invalid_prefixed_parent_can_create_unattributed_children(client):
    response = client.post(
        "/child-barcodes/HT/new",
        data=json.dumps({"barcode": "test-123", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"barcodes": ["HT-111111", "HT-111112", "HT-111113"], "id": 1}}
    assert response.status_code == HTTPStatus.CREATED


def test_new_child_barcode_valid_parent_can_create_attributed_children_and_descendants_can_continue_lineage(client):
    response = client.post(
        "/child-barcodes/HT/new",
        data=json.dumps({"barcode": "HT-1", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"barcodes": ["HT-1-1", "HT-1-2", "HT-1-3"], "id": 1}}
    assert response.status_code == HTTPStatus.CREATED

    response = client.post(
        "/child-barcodes/HT/new",
        data=json.dumps({"barcode": "HT-1-1", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"barcodes": ["HT-1-4", "HT-1-5", "HT-1-6"], "id": 2}}
    assert response.status_code == HTTPStatus.CREATED

    response = client.post(
        "/child-barcodes/HT/new",
        data=json.dumps({"barcode": "HT-1-5", "count": 1}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"barcodes": ["HT-1-7"], "id": 3}}
    assert response.status_code == HTTPStatus.CREATED


def test_new_child_barcode_valid_parent_can_create_attributed_children_and_children_and_parent_can_continue_lineage(
    client,
):
    # Parent
    response = client.post(
        "/child-barcodes/HT/new",
        data=json.dumps({"barcode": "HT-1", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"barcodes": ["HT-1-1", "HT-1-2", "HT-1-3"], "id": 1}}
    assert response.status_code == HTTPStatus.CREATED

    # Children 1
    response = client.post(
        "/child-barcodes/HT/new",
        data=json.dumps({"barcode": "HT-1-1", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"barcodes": ["HT-1-4", "HT-1-5", "HT-1-6"], "id": 2}}
    assert response.status_code == HTTPStatus.CREATED

    # Children 2
    response = client.post(
        "/child-barcodes/HT/new",
        data=json.dumps({"barcode": "HT-1-2", "count": 2}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"barcodes": ["HT-1-7", "HT-1-8"], "id": 3}}
    assert response.status_code == HTTPStatus.CREATED

    # Parent again
    response = client.post(
        "/child-barcodes/HT/new",
        data=json.dumps({"barcode": "HT-1", "count": 2}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"barcodes": ["HT-1-9", "HT-1-10"], "id": 4}}
    assert response.status_code == HTTPStatus.CREATED


def test_new_child_barcode_invalid_parent_can_create_unattributed_children(client):
    response = client.post(
        "/child-barcodes/HT/new",
        data=json.dumps({"barcode": "HT1-1", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"barcodes": ["HT-111111", "HT-111112", "HT-111113"], "id": 1}}
    assert response.status_code == HTTPStatus.CREATED


def test_new_child_barcode_invalid_parent_can_create_unattributed_children_several_times(client):
    response = client.post(
        "/child-barcodes/HT/new",
        data=json.dumps({"barcode": "HT1-1", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"barcodes": ["HT-111111", "HT-111112", "HT-111113"], "id": 1}}
    assert response.status_code == HTTPStatus.CREATED

    response = client.post(
        "/child-barcodes/HT/new",
        data=json.dumps({"barcode": "HT1-1", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"barcodes": ["HT-111114", "HT-111115", "HT-111116"], "id": 2}}
    assert response.status_code == HTTPStatus.CREATED


def test_new_child_barcode_unattributed_children_of_invalid_parent_can_start_own_lineage(client):
    # invalid parent
    response = client.post(
        "/child-barcodes/HT/new",
        data=json.dumps({"barcode": "HT1-1", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"barcodes": ["HT-111111", "HT-111112", "HT-111113"], "id": 1}}
    assert response.status_code == HTTPStatus.CREATED

    # unattributed_children
    response = client.post(
        "/child-barcodes/HT/new",
        data=json.dumps({"barcode": "HT-111111", "count": 2}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"barcodes": ["HT-111111-1", "HT-111111-2"], "id": 2}}
    assert response.status_code == HTTPStatus.CREATED

    # new lineage
    response = client.post(
        "/child-barcodes/HT/new",
        data=json.dumps({"barcode": "HT-111111-2", "count": 2}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"barcodes": ["HT-111111-3", "HT-111111-4"], "id": 3}}
    assert response.status_code == HTTPStatus.CREATED


def test_new_child_barcode_impostor_children_with_possible_parent_can_be_stopped(client):
    # invalid parent
    response = client.post(
        "/child-barcodes/HT/new",
        data=json.dumps({"barcode": "HT-1", "count": 2}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"barcodes": ["HT-1-1", "HT-1-2"], "id": 1}}
    assert response.status_code == HTTPStatus.CREATED

    # Hacking children
    response = client.post(
        "/child-barcodes/HT/new",
        data=json.dumps({"barcode": "HT-1-3", "count": 1}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"errors": ["InvalidParentBarcode"]}
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


def test_new_child_barcode_impostor_children_without_possible_parent_can_be_stopped(client):
    # Hacking children
    response = client.post(
        "/child-barcodes/HT/new",
        data=json.dumps({"barcode": "HT-1-3", "count": 1}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"errors": ["InvalidParentBarcode"]}
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


def test_new_child_barcode_children_of_invalid_parent_can_create_children(client):
    response = client.post(
        "/child-barcodes/HT/new",
        data=json.dumps({"barcode": "HT1-1", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"barcodes": ["HT-111111", "HT-111112", "HT-111113"], "id": 1}}
    assert response.status_code == HTTPStatus.CREATED

    response = client.post(
        "/child-barcodes/HT/new",
        data=json.dumps({"barcode": "HT-111111", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"barcodes_group": {"barcodes": ["HT-111111-1", "HT-111111-2", "HT-111111-3"], "id": 2}}
    assert response.status_code == HTTPStatus.CREATED


def test_new_child_barcode_with_unknown_prefix_rejects_request(client):
    response = client.post(
        "/child-barcodes/unknown/new",
        data=json.dumps({"barcode": "SANG-1", "count": 3}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"errors": ["InvalidPrefixError"]}
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


def test_no_child_barcode(client):
    response = client.post(
        "/child-barcodes/test/new", data=json.dumps({}), headers={"Content-Type": "application/json"}
    )
    assert response.json == {"errors": ["InvalidBarcodeError"]}
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_bad_child_barcode(client):
    response = client.post(
        "/child-barcodes/test/new", data=json.dumps({"barcode": " "}), headers={"Content-Type": "application/json"}
    )
    assert response.json == {"errors": ["InvalidBarcodeError"]}
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_bad_count(client):
    response = client.post(
        "/child-barcodes/test/new",
        data=json.dumps({"barcode": "test", "count": 0}),
        headers={"Content-Type": "application/json"},
    )
    assert response.json == {"errors": ["InvalidCountError"]}
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


# def test_child_barcodes_use_previous_parent_when_present_allowed(app):
#     with app.app_context():
#         # Create a barcode record in the database
#         create_child_barcodes("SQPD-1234", 5)
#         # Expect child barcode to have correct when suffix when same barcode is used
#         assert create_child_barcodes("SQPD-1234", 1) == ["SQPD-1234-6"]
#         assert create_child_barcodes("DN1234", 2) == ["DN1234-1", "DN1234-2"]


# def test_child_barcodes_use_child_format_when_parent_was_a_child(app):
#     with app.app_context():
#         # Create a barcode record in the database
#         create_child_barcodes("SQPD-1234", 5)
#         # Expect child barcode to have correct when suffix when same barcode is used
#         expected_child_barcodes = ["SQPD-1234-6"]
#         assert create_child_barcodes("SQPD-1234-5", 1) == expected_child_barcodes

# def test_child_barcodes_use_standard_format_when_parent_not_allowed(app):
#     with app.app_context():
#         # Create a barcode record in the database
#         create_child_barcodes("SQPD-1234", 5)
#         # Expect child barcode to have correct when suffix when same barcode is used
#         expected_child_barcodes = ["SQPD-1"]
#         assert create_child_barcodes("AA-12345", 1) == expected_child_barcodes
