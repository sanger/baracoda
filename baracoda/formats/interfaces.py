from baracoda.exceptions import UnsupportedChildrenCreation


class FormatterInterface:
    def barcode(self, value: int) -> str:
        pass

    def child_barcode(self, parent_barcode: str, pos: int) -> str:
        raise UnsupportedChildrenCreation(
            "The Barcode formatter class provided does not implement barcode children creation"
        )
