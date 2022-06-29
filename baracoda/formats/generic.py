from baracoda.formats.interfaces import FormatterInterface
from baracoda.exceptions import UnsupportedEncodingForPrefix
import logging

logger = logging.getLogger(__name__)


class GenericBarcodeFormatter(FormatterInterface):
    def __init__(self, prefix: str):
        logger.debug(f"Instantiate formatter with {prefix}")
        if not prefix.isascii():
            raise UnsupportedEncodingForPrefix("The prefix provided {prefix} is not ASCII")

        self.prefix = prefix

    def barcode(self, value: int) -> str:
        """
        Method which returns a barcode formatted with a prefix.

        Arguments:
            value {str} -- the value of the barcode from the sequence

        Returns:
            str -- formatted barcode with prefix and checksum
        """

        return f"{self.prefix}-{value}"
