from baracoda.formats.interfaces import FormatterInterface
from baracoda.exceptions import UnsupportedEncodingForPrefix
import logging

logger = logging.getLogger(__name__)


class Sequencescape22Formatter(FormatterInterface):
    CHECKSUM_ASCII_OFFSET = 65

    def __init__(self, prefix: str):
        logger.debug(f"Instantiate formatter with {prefix}")
        if not prefix.isascii():
            raise UnsupportedEncodingForPrefix("The prefix provided {prefix} is not ASCII")

        self.prefix = prefix

    def barcode(self, value: int) -> str:
        """
        Method which returns a barcode with a prefix.
        If the barcode needs to be converted it is formatted otherwise it is returned as is

        Arguments:
            value {str} -- the value of the barcode from the sequence

        Returns:
            str -- formatted barcode with prefix and checksum
        """

        return self.barcode_with_checksum(f"{self.prefix}-{value}")

    def suffix(self, barcode: str) -> str:
        """
        Calculates the checksum suffix for a barcode

        Arguments:
            barcode {str} -- the barcode we want to calculate the checksum from

        Returns:
            str -- single character with the checksum for the string received as param
        """
        sum = 0
        pos = 0

        for char in reversed(barcode):
            sum += ord(char) * (pos + 1)
            pos += 1

        return chr((sum % 23) + self.CHECKSUM_ASCII_OFFSET)

    def child_barcode(self, parent_barcode: str, pos: int) -> str:
        """
        Returns the valid format for a child_barcode using this formatter.

        Arguments:
            parent_barcode {str} -- parent barcode we want to generate child barcode from
            pos -- number of children to generate

        Returns:
            str -- string representation of the child barcode
        """
        return self.barcode_with_checksum(f"{parent_barcode}-{pos}")

    def barcode_with_checksum(self, barcode: str) -> str:
        """
        Returns the passed argument barcode with a checksum attached as a suffix with '-'

        Arguments:
            barcode {str} -- the barcode we want to attach a suffix

        Returns:
            str -- the same barcode but with the suffix attached separated by '-'
        """
        return f"{ barcode }-{ self.suffix(barcode) }"
