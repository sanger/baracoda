from baracoda.formats.interfaces import FormatterInterface
from baracoda.exceptions import UnsupportedEncodingForPrefix
import logging
from typing import Dict

logger = logging.getLogger(__name__)


class GenericBarcodeFormatter(FormatterInterface):
    def __init__(self, options: Dict[str, str]):
        super().extract_options(options)
        logger.debug(f"Instantiate formatter with {self.prefix}")
        if not self.prefix.isascii():
            raise UnsupportedEncodingForPrefix("The prefix provided {self.prefix} is not ASCII")

    def barcode(self, value: int) -> str:
        """
        Method which returns a barcode formatted with a prefix.

        Arguments:
            value {str} -- the value of the barcode from the sequence

        Returns:
            str -- formatted barcode with prefix and checksum
        """

        return f"{self.prefix}-{value}"
