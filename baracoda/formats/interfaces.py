from baracoda.exceptions import UnsupportedChildrenCreation, UnsupportedTextCodeValue
from typing import Dict
import re


class FormatterInterface:
    """Interface class that requires to be implemented to support
    a new barcode format.
    """

    def barcode(self, value: int) -> str:
        raise NotImplementedError("The Barcode formatter class provided does not implement the barcode method.")

    def child_barcode(self, parent_barcode: str, pos: int) -> str:
        raise UnsupportedChildrenCreation(
            "The Barcode formatter class provided does not implement barcode children creation."
        )

    def extract_options(self, options: Dict[str, str]) -> None:
        self.prefix = options["prefix"]

        self._extract_text(options)

    def _extract_text(self, options: Dict[str, str]) -> None:
        self.text = None
        if ("text" in options) and (options["text"] is not None):
            regexp = re.compile("^[a-zA-Z0-9_]{1,3}$")
            if regexp.match(options["text"]) is None:
                raise UnsupportedTextCodeValue()

            self.text = options["text"]
