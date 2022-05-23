from typing import Dict, List, Union
from baracoda.formats import HeronCogUkIdFormatter, GenericBarcodeFormatter

PREFIXES: List[Dict[str, Union[str, object]]] = [
    {
        "prefix": "SANG",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "CAMB",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "NORW",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "NOTT",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "LEED",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "HT",
        "sequence_name": "ht",
        "formatter_class": GenericBarcodeFormatter,
        "enableChildrenCreation": False,
    },
    {
        "prefix": "SQPD",
        "sequence_name": "sqp",
        "formatter_class": GenericBarcodeFormatter,
        "enableChildrenCreation": True,
    },
]
