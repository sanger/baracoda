import logging
from http import HTTPStatus
from typing import Any, Tuple

from flask import Blueprint, current_app, request, g

from baracoda.exceptions import InvalidPrefixError
from baracoda.operations import BarcodeOperations

bp = Blueprint("barcode_creation", __name__)

logger = logging.getLogger(__name__)


@bp.route("/barcodes_group/<prefix>/new", methods=["POST"])
def get_new_barcode_group(prefix: str) -> Tuple[Any, int]:
    try:
        count = get_count_param()

        operator = BarcodeOperations(
            prefix=prefix, sequence_name=current_app.config["SEQUENCE_NAME"]
        )
        # count = 1
        barcode_group = operator.create_barcode_group(count)
        return (
            barcode_group.to_hash(),
            HTTPStatus.CREATED,
        )

    except InvalidPrefixError as e:
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route("/barcodes/<prefix>/new", methods=["POST"])
def get_new_barcode(prefix: str) -> Tuple[Any, int]:
    try:
        operator = BarcodeOperations(
            prefix=prefix, sequence_name=current_app.config["SEQUENCE_NAME"]
        )
        barcode = operator.create_barcode()

        return barcode.to_hash(), HTTPStatus.CREATED

    except InvalidPrefixError as e:
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route("/barcodes/<prefix>/last", methods=["GET"])
def get_last_barcode(prefix: str) -> Tuple[Any, int]:
    try:
        operator = BarcodeOperations(
            prefix=prefix, sequence_name=current_app.config["SEQUENCE_NAME"]
        )

        barcode = operator.get_last_barcode(prefix)
        if barcode is None:
            return "", HTTPStatus.NOT_FOUND
        return barcode.to_hash(), HTTPStatus.OK

    except InvalidPrefixError as e:
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.INTERNAL_SERVER_ERROR


def get_count_param():
    if "count" in request.values:
        return int(request.values["count"])
    else:
        return int(request.json["count"])
