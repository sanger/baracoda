def default_config():
    return { 
        'prefixes': [
            {
                'prefix': 'SANG',
                'description': 'Sanger barcodes',
                'sequence_start': 1
            },
            {
                'prefix': 'NIRE',
                'description': 'Nire barcodes',
                'sequence_start': 1
            }
        ],
        'valid_prefixes': ['SANG', 'NIRE']
    }

def development_config():
    return default_config()

def testing_config():
    return default_config()

def production_config():
    return default_config()
