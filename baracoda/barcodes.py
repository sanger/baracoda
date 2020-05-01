import logging
from http import HTTPStatus
from typing import Any, Tuple

from flask import Blueprint, current_app

from baracoda.exceptions import InvalidPrefixError
from baracoda.operations import BarcodeOperations

bp = Blueprint("barcode_creation", __name__)

logger = logging.getLogger(__name__)


@bp.route("/barcodes/<prefix>/new", methods=["POST"])
def get_next_barcode(prefix: str) -> Tuple[Any, int]:
    try:
        operator = BarcodeOperations(
            prefix=prefix, sequence_name=current_app.config["SEQUENCE_NAME"]
        )

        barcode = operator.generate_barcode()

        return {"barcode": barcode}, HTTPStatus.CREATED

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
        return {"barcode": barcode}, HTTPStatus.OK

    except InvalidPrefixError as e:
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.INTERNAL_SERVER_ERROR
