def development_config():
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

def testing_config():
    return { 
        'prefixes': [
            {
                'prefix': 'SANG',
                'description': 'Sanger barcodes',
                'sequence_start': 1,
                'reset_sequence': True
            },
            {
                'prefix': 'NIRE',
                'description': 'Nire barcodes',
                'sequence_start': 1,
                'reset_sequence': True
            }
        ],
        'valid_prefixes': ['SANG', 'NIRE']
    }

def production_config():
    return development_config()
