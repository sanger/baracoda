import xml.etree.ElementTree as ET
import re

def test_hello(client):
    response = client.get('/testing')
    root = ET.fromstring(response.data)
    print(root.tag)
    assert root.tag == 'plate_barcodes'
    assert root[0].tag == 'barcode'

    pattern = re.compile('^\d+$')
    assert pattern.match(root[0].text) is not None
