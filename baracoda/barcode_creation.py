from flask import Blueprint, jsonify, request, current_app

from baracoda import db
from baracoda.exceptions import WrongPrefixError
from baracoda.barcode_formats import HeronFormatter

bp = Blueprint("barcode_creation", __name__)

def validate_prefix(prefix):
    return (prefix in current_app.config['valid_prefixes'])

def endpoint_for_barcode_render(prefix, barcode_index_generator, status_code_success):
    if not validate_prefix(prefix):
        return jsonify({'errors': ['The provided prefix is not allowed']}), 403

    try:
        formatter = HeronFormatter({"prefix": prefix})
    except WrongPrefixError as error:
        return jsonify({'errors': [str(error)]}), 422

    next_value = barcode_index_generator(prefix)

    hex_str = format(next_value, 'X')
    barcode = formatter.barcode(hex_str)

    return (jsonify({'barcode': barcode}), status_code_success)


@bp.route('/prefix/<prefix>/new', methods=['POST'])
def get_next_barcode(prefix):
    return endpoint_for_barcode_render(prefix, db.get_next_value, 201)

@bp.route('/prefix/<prefix>/last', methods=['GET'])
def get_last_barcode(prefix):
    return endpoint_for_barcode_render(prefix, db.get_current_value, 200)