import logging
from http import HTTPStatus
from typing import Any, Tuple

from flask import Blueprint, request
from sqlalchemy import exc
from flask_cors import CORS
import pdb
from baracoda.operations import ChildBarcodeOperations
from baracoda.exceptions import InvalidCountError

bp = Blueprint("child_barcode_creation", __name__)
CORS(bp)

logger = logging.getLogger(__name__)


@bp.post("/child-barcodes/create")  # type: ignore
def create_child_barcodes() -> Tuple[Any, int]:
    try:
        count = request.args.get('count', default=1, type=int)
        barcode = request.args.get('barcode', default=1, type=str)
        logger.debug(f"Creating child barcode(s) for '{barcode}'")

        child_barcodes = ChildBarcodeOperations.create_child_barcodes(barcode, count)

        return (
            { "barcodes": child_barcodes },
            HTTPStatus.CREATED,
        )
    except InvalidCountError as e:
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.UNPROCESSABLE_ENTITY
    except exc.IntegrityError as e:
        logger.error(f"{type(e).__name__}: Two creation requests recieved for the same barcode")
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        return {"errors": [f"{type(e).__name__}"]}, HTTPStatus.INTERNAL_SERVER_ERROR