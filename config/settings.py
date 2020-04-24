def development_config():
    return {
        "sequence_name": "heron",
        "sequence_start": 200000,
    }


def testing_config():
    return {"sequence_name": "heron", "sequence_start": 200000, "reset_sequence": True}


def production_config():
    return development_config()
