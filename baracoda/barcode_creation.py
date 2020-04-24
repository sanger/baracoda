from flask import Blueprint, jsonify, request, current_app

from baracoda.barcode_operations import BarcodeOperations
from baracoda.exceptions import ValidationError

bp = Blueprint("barcode_creation", __name__)


@bp.route("/barcodes/<prefix>/new", methods=["POST"])
def get_next_barcode(prefix):
    try:
        count = get_count(request)

        operator = BarcodeOperations(
            {
                "prefix": prefix,
                "count": count,
                "sequence_name": current_app.config["sequence_name"],
            }
        )

        records = operator.generate_barcodes()
        if len(records) == 1:
            records = records[0]
        return (jsonify(records), 201)

    except ValidationError as error:
        return jsonify({"errors": [str(error)]}), 422


@bp.route("/barcodes/<prefix>/last", methods=["GET"])
def get_last_barcode(prefix):
    try:
        operator = BarcodeOperations(
            {"prefix": prefix, "sequence_name": current_app.config["sequence_name"]}
        )

        barcode = operator.get_last_barcode(prefix)

        if barcode is None:
            return 404
        return (jsonify({"barcode": barcode}), 200)

    except ValidationError as error:
        return jsonify({"errors": [str(error)]}), 422


def get_count(request):
    if len(request.data) > 0 and ("count" in request.json):
        return request.json["count"]
    else:
        return 1
