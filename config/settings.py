def development_config():
    return {
        "prefixes": [
            {
                "prefix": "SANG",
                "description": "Sanger barcodes",
                "centre": "Sanger Institute",
            },
            {"prefix": "NIRE", "description": "Nire barcodes", "centre": "Nire"},
        ],
        "valid_prefixes": ["SANG", "NIRE"],
        "sequence_name": "heron",
        "sequence_start": 200000,
    }


def testing_config():
    return {
        "prefixes": [
            {
                "prefix": "SANG",
                "description": "Sanger barcodes",
                "centre": "Sanger Institute",
            },
            {"prefix": "NIRE", "description": "Nire barcodes", "centre": "Nire"},
        ],
        "valid_prefixes": ["SANG", "NIRE"],
        "sequence_name": "heron",
        "sequence_start": 200000,
        "reset_sequence": True,
    }


def production_config():
    return development_config()
