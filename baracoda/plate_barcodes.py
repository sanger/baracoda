import logging
from flask import Blueprint
from http import HTTPStatus
from typing import Any, Tuple
from baracoda.exceptions import InvalidPrefixError
from baracoda.operations import BarcodeOperations
from dicttoxml import dicttoxml

bp = Blueprint("plate_barcode_creation", __name__)

logger = logging.getLogger(__name__)

SEQ_DNAPLATE_PREFIX = "DN"


@bp.post("/plate_barcodes.xml")  # type: ignore
def get_new_plate_barcode() -> Tuple[Any, int]:
    try:
        logger.debug(f"Creating a plate_barcode.xml")
        operator = BarcodeOperations(prefix=SEQ_DNAPLATE_PREFIX)
        barcode = operator.create_barcode()
        response = dicttoxml(barcode.to_dict(), attr_type=False, custom_root="plate_barcode")

        return response, HTTPStatus.OK

    except InvalidPrefixError as e:
        return dicttoxml([f"{type(e).__name__}"], attr_type=False, custom_root="errors"), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return (
            dicttoxml([f"{type(e).__name__}"], attr_type=False, custom_root="errors"),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
