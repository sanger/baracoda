import logging
import re
from datetime import datetime
from typing import List, Optional, cast
from baracoda.db import db
from baracoda.exceptions import InvalidPrefixError
from baracoda.helpers import get_prefix_item
from baracoda.orm.barcode import Barcode
from baracoda.orm.child_barcode import ChildBarcode
from baracoda.orm.barcodes_group import BarcodesGroup
from baracoda.formats import FormatterInterface
from baracoda.types import PrefixesType

logger = logging.getLogger(__name__)


class BarcodeOperations:
    def __init__(self, prefix: str):
        logger.debug("Instantiate....")

        self.prefix = prefix

        self.__check_prefix()

        logger.debug(f"Setting prefix item from prefix {self.prefix}")
        self.__set_prefix_item()

        # if the prefix item does not exist the prefix is not valid
        if self.prefix_item is None:
            raise InvalidPrefixError()

        # saves pulling it out of object every time
        logger.debug("Accessing sequence_name")
        self.sequence_name = self.prefix_item["sequence_name"]

    def formatter(self) -> FormatterInterface:
        formatter_class = cast(PrefixesType, self.prefix_item)["formatter_class"]
        return formatter_class(self.prefix)

    def create_barcode_group(self, count: int) -> BarcodesGroup:
        """Creates a new barcode group and the associated barcodes.

        Arguments:
            count {int} -- number of barcodes to create in the group

        Returns:
            BarcodeGroup -- the barcode group created
        """
        try:
            next_values = self.__get_next_values(self.sequence_name, count)

            barcodes_group = self.__build_barcodes_group()
            db.session.add(barcodes_group)

            barcodes = [
                self.__build_barcode(self.prefix, next_value, barcodes_group=barcodes_group)
                for next_value in next_values
            ]
            db.session.add_all(barcodes)

            db.session.commit()

            return barcodes_group
        except Exception as e:
            db.session.rollback()
            raise e

    def create_barcode(self) -> Barcode:
        """Generate and store a barcode using the Heron formatter.

        Returns:
            str -- the generated barcode in the Heron format
        """
        logger.debug(f"Calling create_barcode for sequence name {self.sequence_name}")
        try:
            next_value = self.__get_next_value(self.sequence_name)
            barcode = self.__build_barcode(self.prefix, next_value, barcodes_group=None)

            db.session.add(barcode)

            db.session.commit()

            return barcode
        except Exception as e:
            db.session.rollback()
            raise e

    def get_last_barcode(self, prefix: str) -> Optional[Barcode]:
        """Get the last barcode generated for the specified sequence.

        Arguments:
            prefix {str} -- prefix to use query for the last barcode

        Returns:
            Barcode -- last barcode generated for prefix or None
        """
        results = (
            db.session.query(Barcode, Barcode.barcode).filter_by(prefix=self.prefix).order_by(Barcode.id.desc()).first()
        )

        if results is None:
            return results

        return cast(Barcode, results[0])

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

    def __build_barcode(self, prefix: str, next_value: int, barcodes_group: Optional[BarcodesGroup]) -> Barcode:
        barcode = self.formatter().barcode(next_value)
        return Barcode(
            prefix=prefix,
            barcode=barcode,
            created_at=datetime.now(),
            barcodes_group=barcodes_group,
        )

    def __build_barcodes_group(self) -> BarcodesGroup:
        return BarcodesGroup(created_at=datetime.now())

    def __get_next_value(self, sequence_name: str) -> int:
        """Get the next value from the sequence.

        Arguments:
            sequence_name {str} -- name of the sequence to query

        Returns:
            str -- next value in sequence
        """
        return int(db.session.execute(f"SELECT nextval('{sequence_name.lower()}');").fetchone()[0])

    def __get_next_values(self, sequence_name: str, count: int) -> List[int]:
        """Get the next count values from the sequence.

        Arguments:
            sequence_name {str} -- name of the sequence to query
            count {int} -- number of values from the sequence to generate

        Returns:
            str -- next value in sequence
        """
        return [
            int(val[0])
            for val in db.session.execute(
                f"SELECT nextval('{sequence_name.lower()}') FROM    generate_series(1, {count}) l;"
            ).fetchall()
        ]

    def __set_prefix_item(self):
        """Get the prefix details.

        Returns:
            prefix item or None if prefix does not exist
        """
        self.prefix_item = get_prefix_item(self.prefix)


class ChildBarcodeOperations:
    @staticmethod
    def create_child_barcodes(barcode: str, count: int) -> List[str]:
        """Retrieve the next child barcodes for a given barcode

        Returns:
            [str] -- The generated child barcodes
        """

        try:
            # Check barcode exists
            barcode_record = db.session.query(ChildBarcode).with_for_update().filter_by(barcode=barcode).first()

            # If no record, then create one
            if barcode_record is None:
                old_count = 0
                barcode_record = ChildBarcode(barcode=barcode, child_count=count)
                db.session.add(barcode_record)
            else:
                old_count = barcode_record.child_count
                barcode_record.child_count = old_count + count

            db.session.commit()

            # We want the new count to start at the next number
            new_count = old_count + 1

            # Format child barcodes
            child_barcodes = []
            for x in range(new_count, barcode_record.child_count + 1):
                child_barcodes.append(f"{barcode}-{x}")

            return child_barcodes
        except Exception as e:
            db.session.rollback()
            raise e
