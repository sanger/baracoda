import logging
from http import HTTPStatus
from typing import Any, Tuple

from flask import Blueprint, request
from flask_cors import CORS

from baracoda.exceptions import InvalidCountError, InvalidPrefixError
from werkzeug.exceptions import BadRequest
from baracoda.operations import BarcodeOperations

bp = Blueprint("barcode_creation", __name__)
CORS(bp)

logger = logging.getLogger(__name__)


@bp.post("/barcodes_group/<prefix>/new")  # type: ignore
def get_new_barcode_group(prefix: str) -> Tuple[Any, int]:
    try:
        count = get_count_param()

        operator = BarcodeOperations(prefix=prefix)
        barcode_group = operator.create_barcode_group(count)
        return (
            barcode_group.to_dict(),
            HTTPStatus.CREATED,
        )

    except InvalidPrefixError as e:
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.BAD_REQUEST
    except InvalidCountError as e:
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.UNPROCESSABLE_ENTITY
    except BadRequest as e:
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.INTERNAL_SERVER_ERROR


@bp.post("/barcodes/<prefix>/new")  # type: ignore
def get_new_barcode(prefix: str) -> Tuple[Any, int]:
    try:
        operator = BarcodeOperations(prefix=prefix)
        barcode = operator.create_barcode()

        return barcode.to_dict(), HTTPStatus.CREATED

    except InvalidPrefixError as e:
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.INTERNAL_SERVER_ERROR


@bp.get("/barcodes/<prefix>/last")  # type: ignore
def get_last_barcode(prefix: str) -> Tuple[Any, int]:
    try:
        operator = BarcodeOperations(prefix=prefix)

        barcode = operator.get_last_barcode(prefix)
        if barcode is None:
            return "", HTTPStatus.NOT_FOUND
        return barcode.to_dict(), HTTPStatus.OK

    except InvalidPrefixError as e:
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.INTERNAL_SERVER_ERROR


def positive_value(value: int) -> int:
    """Returns the value passed as argument if is a positive higher than zero
    or raise exception if not.
    Arguments:
        value : int - Value to check

    Returns:
        value : same value passed as input or
        InvalidCountError exception if not
    """
    if value > 0:
        return value
    raise InvalidCountError()


def get_count_param():
    if "count" in request.values:
        return positive_value(int(request.values["count"]))
    else:
        try:
            if request.json and ("count" in request.json):
                return positive_value(int(request.json["count"]))
        except BadRequest as e:
            raise e
    raise InvalidCountError()
