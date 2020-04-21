from flask import Blueprint, jsonify, request

from baracoda import db
from baracoda.exceptions import WrongPrefixError
from baracoda.barcode_formats import HeronFormatter

bp = Blueprint("barcode_creation", __name__)

@bp.route('/cog/new', methods=['POST'])
def get_next_barcode():
    try:
        formatter = HeronFormatter(request.get_json())
    except WrongPrefixError as error:
        return jsonify({'errors': [str(error)]}), 422

    next_value = db.get_next_value()
    hex_str = format(next_value, 'X')
    barcode = formatter.barcode(hex_str)

    return (jsonify({'barcode': barcode}), 201)

