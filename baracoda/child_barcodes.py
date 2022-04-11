import logging
from http import HTTPStatus
from typing import Any, Tuple

from flask import Blueprint, request
from sqlalchemy import exc
from flask_cors import CORS
from baracoda.operations import ChildBarcodeOperations
from baracoda.exceptions import InvalidCountError, InvalidBarcodeError

bp = Blueprint("child_barcode_creation", __name__)
CORS(bp)

logger = logging.getLogger(__name__)


@bp.post("/child-barcodes/new")  # type: ignore
def create_child_barcodes() -> Tuple[Any, int]:
    try:
        count = get_count_param()
        barcode = get_barcode_param()

        logger.debug(f"Creating child barcode(s) for '{barcode}'")
        child_barcodes = ChildBarcodeOperations.create_child_barcodes(barcode, count)

        return (
            {"barcodes": child_barcodes},
            HTTPStatus.CREATED,
        )
    except InvalidCountError as e:
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.UNPROCESSABLE_ENTITY
    except InvalidBarcodeError as e:
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.UNPROCESSABLE_ENTITY
    except exc.IntegrityError as e:
        logger.error(f"{type(e).__name__}: Two creation requests recieved for the same barcode")
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.INTERNAL_SERVER_ERROR


def get_count_param():
    count = 1  # Default count
    if "count" in request.values:
        count = int(request.values["count"])
    else:
        if request.json and ("count" in request.json):
            count = int(request.json["count"])
    if count > 0:
        return count
    raise InvalidCountError()


def get_barcode_param():
    barcode = ""
    if "barcode" in request.values:
        barcode = str(request.values["barcode"])
    else:
        if request.json and ("barcode" in request.json):
            barcode = str(request.json["barcode"])
    if len(barcode.strip()) > 0:
        return barcode
    raise InvalidBarcodeError()
