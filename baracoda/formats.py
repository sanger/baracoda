import logging

logger = logging.getLogger(__name__)

class HeronFormatter:
    def __init__(self, prefix: str, convert: bool = True):
        logger.debug(f"Instantiate formatter with {prefix}")

        self.prefix = prefix
        self.convert = convert

    def hex_to_int(self, hex_str: str) -> int:
        """Convert a hex string to integer.

        Arguments:
            hex_str {str} -- hex string to convert

        Returns:
            int -- integer representation of the hex value
        """
        return int(hex_str, 16)

    def checksum(self, hex_str: str) -> str:
        """Calculates a checksum from the given hex string.

        Arguments:
            hex_str {str} -- hexidecimal string used to create checksum

        Returns:
            str -- checksum value
        """
        pos = 0
        even = odd = 0

        for char in reversed(hex_str):
            if (pos % 2) == 0:
                even += self.hex_to_int(char)
            else:
                odd += self.hex_to_int(char)
            pos += 1

        val = ((odd * 3) + even) % 16

        """
        format into hex
        https://docs.python.org/3/library/string.html#format-specification-mini-language
        "Hex format. Outputs the number in base 16, using upper-case letters for the digits above
        9."
        """
        if val != 0:
            return format((16 - val), "X")
        else:
            return format(val, "X")

    def barcode(self, value: int) -> str:
        """
        Method which returns a barcode with a prefix.
        If the barcode needs to be converted it is formatted otherwise it is returned as is

        Arguments:
            value {str} -- the value of the barcode from the sequence

        Returns:
            str -- formatted barcode with prefix and checksum
        """

        formatted_value = self.format_barcode_number(value) if self.convert else value

        return f"{self.prefix}-{formatted_value}"

    def format_barcode_number(self, value: int) -> str:
        """Method which returns a barcode with the prefix and checksum.

        Arguments:
            value {str} -- the value of the barcode from the sequence

        Returns:
            str -- formatted barcode with prefix and checksum
        """
        hex_str = format(value, 'X')
        return f"{hex_str}{self.checksum(hex_str)}"
