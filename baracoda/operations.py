import logging
import re
from datetime import datetime
from typing import Optional

from baracoda.db import get_db
from baracoda.exceptions import InvalidPrefixError
from baracoda.formats import HeronFormatter

logger = logging.getLogger(__name__)


class BarcodeOperations:
    def __init__(self, sequence_name: str, prefix: str):
        logger.debug("Instantiate....")
        self.sequence_name = sequence_name
        self.prefix = prefix

        self.__check_prefix()

        self.formatter = HeronFormatter(prefix=self.prefix)

    def generate_barcode(self) -> str:
        """Generate and store a barcode using the Heron formatter.

        Returns:
            str -- the generated barcode in the Heron format
        """
        db = get_db()

        with db.connection:
            with db.cursor as self.__cursor:
                next_value = self.__get_next_value(self.sequence_name)

                #  convert the next value to hexidecimal
                hex_str = format(next_value, "X")
                barcode = self.formatter.barcode(hex_str)

                self.__store_barcode(barcode)

        return barcode

    def get_last_barcode(self, prefix: str) -> Optional[str]:
        """Get the last barcode generated for the specified sequence.

        Arguments:
            prefix {str} -- prefix to use query for the last barcode

        Returns:
            Optional[str] -- last barcode generated for prefix or None
        """
        db = get_db()

        with db.connection:
            with db.cursor as self.__cursor:
                last_barcode = self.__get_last_barcode()

        return last_barcode

    def __check_prefix(self) -> None:
        """Checks the provided prefix.

        Raises:
            InvalidPrefixError: the prefix does not pass the regex test
        """
        if not self.__validate_prefix():
            raise InvalidPrefixError()

    def __validate_prefix(self) -> bool:
        """Validate the prefix used for the Heron barcodes. Currently accepting uppercase letters
        and numbers between 1 and 10 characters long.

        Returns:
            bool -- whether the prefix passed validation
        """
        if type(self.prefix) != str:
            return False

        pattern = re.compile(r"^[A-Z0-9]{1,10}$")

        return bool(pattern.match(self.prefix))

    def __store_barcode(self, barcode: str) -> None:
        """Store the barcode, prefix and timestamp to the database for later querying.

        Arguments:
            barcode {str} -- barcode to store
        """
        now = datetime.now()

        values = f"('{barcode}', '{self.prefix}', '{now}')"

        command_str = f"INSERT INTO barcodes (barcode, prefix, created_at) VALUES {values};"

        self.__cursor.execute(command_str)

    def __get_last_barcode(self) -> Optional[str]:
        """Query the database for the last barcode created for the prefix.

        Returns:
            Optional[str] -- last barcode generated for prefix or None
        """

        self.__cursor.execute(
            f"SELECT barcode FROM barcodes "
            f"WHERE barcodes.prefix='{self.prefix}' "
            "ORDER BY id DESC "
            "LIMIT 1;"
        )

        if result := self.__cursor.fetchone():
            return result[0]
        else:
            return None

    def __get_next_value(self, sequence_name: str) -> str:
        """Get the next value from the sequence.

        Arguments:
            sequence_name {str} -- name of the sequence to query

        Returns:
            str -- next value in sequence
        """
        self.__cursor.execute(f"SELECT nextval('{sequence_name.lower()}');")

        result = self.__cursor.fetchone()

        return result[0]
