import json

def test_incorrect_headers(client):
    response = client.post('/cog/new', data=json.dumps({'prefix': 'SANGER'}))
    assert response.status_code == 422

def test_param_missing_prefix_key(client):
    response = client.post('/cog/new', data=json.dumps({'val': 'SANGER'}), headers={'Content-type': 'application/json'})
    assert response.status_code == 422

def test_param_missing_prefix_value(client):
    response = client.post('/cog/new', data=json.dumps({'prefix': None}), headers={'Content-type': 'application/json'})
    assert response.status_code == 422

def test_param_empty_prefix_value(client):
    response = client.post('/cog/new', data=json.dumps({'prefix': ''}), headers={'Content-type': 'application/json'})
    assert response.status_code == 422

def test_param_prefix_value_wrong_charset(client):
    response = client.post('/cog/new', data=json.dumps({'prefix': '*34'}), headers={'Content-type': 'application/json'})
    assert response.status_code == 422

def test_param_prefix_value_whitespace(client):
    response = client.post('/cog/new', data=json.dumps({'prefix': 'SA R'}), headers={'Content-type': 'application/json'})
    assert response.status_code == 422

def test_param_prefix_invalid_length(client):
    longstr = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    response = client.post('/cog/new', data=json.dumps({'prefix': longstr}), headers={'Content-type': 'application/json'})
    assert response.status_code == 422

def test_param_prefix_valid_length(client):
    longstr = "ABCDEFGHIJ"
    response = client.post('/cog/new', data=json.dumps({'prefix': longstr}), headers={'Content-type': 'application/json'})
    assert response.status_code == 201

def test_get_new_barcode(client):
    response = client.post('/cog/new', data=json.dumps({'prefix': 'SANGER'}), headers={'Content-type': 'application/json'})
    assert response.json == {'barcode': 'SANGER-1F'}
    assert response.status_code == 201
