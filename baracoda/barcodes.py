import logging
from http import HTTPStatus
from typing import Any, Tuple

from flask import Blueprint, request
from flask_cors import CORS

from baracoda.exceptions import InvalidCountError, InvalidPrefixError, InvalidTextError
from werkzeug.exceptions import BadRequest
from baracoda.operations import BarcodeOperations

bp = Blueprint("barcode_creation", __name__)
CORS(bp)

logger = logging.getLogger(__name__)


@bp.post("/barcodes_group/<prefix>/new")  # type: ignore
def get_new_barcode_group(prefix: str) -> Tuple[Any, int]:
    """Endpoint that creates a new group of barcodes that are related in one request

    Arguments:
        - prefix : str - URL extracted argument, that defines the Prefix to use for
          the barcodes generated. It has to be one of the prefixes defined in
          baracoda.config PREFIXES variable
        - count : str - URL or BODY extracted argument. It represents the number of
          barcodes we want to create inside the group.
          If specified in URL it can be defined as url parameter:
            Eg: /barcodes_group/TEST/new?count=14
          If specified in BODY it has to be defined as jSON:
            Eg: { "count": 14 }
    Result:
        - Success: HTTP 201 with JSON representation of BarcodeGroup instance
        - InvalidPrefixError: HTTP 400 with JSON representation of error.
        - InvalidCountError: HTTP 422 with JSON representation of error.
        - OtherError: HTTP 500 with JSON representation of error.
    """
    try:
        logger.debug(f"Creating a barcode group for '{prefix}'")
        count = get_count_param()

        operator = BarcodeOperations(prefix=prefix)
        barcode_group = operator.create_barcode_group(count)
        return (
            barcode_group.to_dict(),
            HTTPStatus.CREATED,
        )

    except InvalidPrefixError as e:
        logger.error(f"{e} {prefix}")
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.BAD_REQUEST
    except InvalidCountError as e:
        logger.error(e)
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.UNPROCESSABLE_ENTITY
    except BadRequest as e:
        logger.error(e)
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        logger.error(e)
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.INTERNAL_SERVER_ERROR


@bp.post("/barcodes/<prefix>/new")  # type: ignore
def get_new_barcode(prefix: str) -> Tuple[Any, int]:
    """Endpoint that creates one single barcode for a prefix

    Arguments:
        - prefix : str - URL extracted argument, that defines the Prefix to use for
          the barcode generated. It has to be one of the prefixes defined in
          baracoda.config PREFIXES variable
    Result:
        - Success: HTTP 201 with JSON representation of Barcode instance
        - InvalidPrefixError: HTTP 400 with JSON representation of error.
        - OtherError: HTTP 500 with JSON representation of error.
    """
    try:
        logger.debug(f"Creating a barcode for '{prefix}'")
        text = get_text_param()
        operator = BarcodeOperations(prefix=prefix, text=text)
        barcode = operator.create_barcode()

        return barcode.to_dict(), HTTPStatus.CREATED

    except InvalidPrefixError as e:
        logger.error(f"{e} {prefix}")
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        logger.error(e)
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.INTERNAL_SERVER_ERROR


@bp.get("/barcodes/<prefix>/last")  # type: ignore
def get_last_barcode(prefix: str) -> Tuple[Any, int]:
    """Endpoint that returns the last generated barcode for a specific prefix

    Arguments:
        - prefix : str - URL extracted argument, that defines the Prefix we want
          to queryu. It has to be one of the prefixes defined in
          baracoda.config PREFIXES variable
    Result:
        - Success: HTTP 200 with JSON representation of barcode instance
        - NotFound: HTTP 404 with empty body
        - InvalidPrefixError: HTTP 400 with JSON representation of error.
        - OtherError: HTTP 500 with JSON representation of error.
    """
    try:
        logger.debug(f"Obtaining last from '{prefix}'")
        operator = BarcodeOperations(prefix=prefix)

        barcode = operator.get_last_barcode(prefix)
        if barcode is None:
            return "", HTTPStatus.NOT_FOUND
        return barcode.to_dict(), HTTPStatus.OK

    except InvalidPrefixError as e:
        logger.error(f"{e} {prefix}")
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        logger.error(e)
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
    raise InvalidCountError("Count value is not a positive integer")


def get_count_param():
    """Extracts the count argument from the HTTP request received.
    If specified in URL it can be defined as url parameter:
    Eg: /barcodes_group/TEST/new?count=14
    If specified in BODY it has to be defined as jSON:
    Eg: { "count": 14 }

    Arguments: No
    Returns one of this:
        int - value of the 'count' argument extracted
        InvalidCountError - Exception raised when argument could not be extracted

    """
    if "count" in request.values:
        try:
            # int can throw an exception if the value is not convertible
            count = int(request.values["count"])
        except ValueError:
            raise InvalidCountError("Count value is not a valid integer")

        return positive_value(count)
    else:
        try:
            if request.json and ("count" in request.json):
                return positive_value(int(request.json["count"]))
        except BadRequest as e:
            raise e
    raise InvalidCountError()


def get_text_param():
    """Extracts the text argument from the HTTP request received.
    If specified in URL it can be defined as url parameter:
    Eg: /barcodes_group/TEST/new?text=T14
    If specified in BODY it has to be defined as jSON:
    Eg: { "text": "T14" }

    Arguments: No
    Returns one of this:
        str[3] - value of the 'text' argument extracted
        InvalidTextError - Exception raised when argument could not be extracted

    """
    if "text" in request.values:
        if len(request.values["text"]) <= 3:
            return request.values["text"]
        raise InvalidTextError()
    else:
        try:
            if request.json and ("text" in request.json):
                return request.json["text"]
        except BadRequest:
            return None

    return None
