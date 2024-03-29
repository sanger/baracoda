from baracoda.formats.heron import HeronCogUkIdFormatter
from baracoda.helpers import get_prefix_item


def test_correct_prefix_item_is_returned(app, prefixes):
    with app.app_context():
        prefix_item = get_prefix_item("LEED")
        assert prefix_item == {
            "prefix": "LEED",
            "sequence_name": "heron",
            "formatter_class": HeronCogUkIdFormatter,
            "enableChildrenCreation": False,
        }


def test_none_is_returned_for_invalid_prefix(app):
    with app.app_context():
        prefix_item = get_prefix_item("MOON")
        assert prefix_item is None
