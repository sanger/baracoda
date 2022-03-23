from typing import Dict, List, Union
from baracoda.formats import HeronCogUkIdFormatter, HeronPlateCherrypickedFormatter

PREFIXES: List[Dict[str, Union[str, bool]]] = [
    {
        "prefix": "SANG",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
    },
    {
        "prefix": "CAMB",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
    },
    {
        "prefix": "NORW",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
    },
    {
        "prefix": "NOTT",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
    },
    {
        "prefix": "LEED",
        "sequence_name": "heron",
        "formatter_class": HeronCogUkIdFormatter,
    },
    {
        "prefix": "HT",
        "sequence_name": "ht",
        "formatter_class": HeronPlateCherrypickedFormatter,
    },
]
