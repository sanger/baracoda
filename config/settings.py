def development_config():
    return { 
        'prefixes': [
            {
                'prefix': 'SANG',
                'description': 'Sanger barcodes'
            },
            {
                'prefix': 'NIRE',
                'description': 'Nire barcodes'
            }
        ],
        'valid_prefixes': ['SANG', 'NIRE'],
        'sequence_name': 'heron',
        'sequence_start': 200000
    }

def testing_config():
    return { 
        'prefixes': [
            {
                'prefix': 'SANG',
                'description': 'Sanger barcodes'
            },
            {
                'prefix': 'NIRE',
                'description': 'Nire barcodes'
            }
        ],
        'valid_prefixes': ['SANG', 'NIRE'],
        'sequence_name': 'heron',
        'sequence_start': 200000,
        'reset_sequence': True
    }

def production_config():
    return development_config()
