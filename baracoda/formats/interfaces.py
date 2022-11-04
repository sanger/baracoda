from baracoda.exceptions import UnsupportedChildrenCreation


class FormatterInterface:
    """Interface class that requires to be implemented to support
    a new barcode format.
    """

    def barcode(self, value: int) -> str:
        pass

    def child_barcode(self, parent_barcode: str, pos: int) -> str:
        raise UnsupportedChildrenCreation(
            "The Barcode formatter class provided does not implement barcode children creation"
        )
