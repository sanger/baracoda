import os
import xml.etree.ElementTree as ET
from . import utils

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        utils.load_config(app)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    @app.route('/hello')
    def hello():
        return "Helllo"

    @app.route('/testing.xml')
    def testing():
        app.logger.info('test')
        plate_barcodes_tag = ET.Element('plate_barcodes')
        barcode_tag = ET.SubElement(plate_barcodes_tag, 'barcode')

        barcode_tag.text = db.get_next_value()

        return ET.tostring(plate_barcodes_tag,
                           encoding="unicode",
                           method='xml',
                           xml_declaration=True)

    return app
