import logging
import re
from datetime import datetime
from typing import List, Optional, cast
from xmlrpc.client import Boolean
from baracoda.db import db
from baracoda.exceptions import InvalidPrefixError
from baracoda.helpers import get_prefix_item
from baracoda.orm.barcode import Barcode
from baracoda.orm.child_barcode import ChildBarcode
from baracoda.orm.barcodes_group import BarcodesGroup
from baracoda.formats.interfaces import FormatterInterface
from baracoda.types import PrefixesType, BarcodeParentInfoType

logger = logging.getLogger(__name__)


class InvalidParentBarcode(BaseException):
    """The barcode provided did not match the right format, or
    it was an impostor barcode (created outside of Baracoda but
    using the same format).
    """

    pass


class InvalidPrefixForChildrenCreation(BaseException):
    """The prefix provided is not currently enabled for children
    creation.
    """

    pass


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
        """Factory method that will create a new formatter instance
        from the prefix declared.

        Returns:
            FormatterInterface instance that can be used to format a new
            barcode string
        """
        formatter_class = cast(PrefixesType, self.prefix_item)["formatter_class"]
        return formatter_class(self.prefix)

    def create_barcodes(self, count: int) -> List[str]:
        """Create a list of barcodes, not inside a group.
        It requests a new list of ids from the sequence associated with the current prefix
        and formats those ids into new barcode strings. The sequence is incremented with this
        request.

        Arguments:
            count - int : number of barcodes to create

        Returns:
            List[str] - List with the string of barcodes created
        """
        next_values = self.__get_next_values(self.sequence_name, count)
        return [self.formatter().barcode(next_value) for next_value in next_values]

    def create_barcode_group(self, count: int) -> BarcodesGroup:
        """Creates a new barcode group and the associated barcodes.

        Arguments:
            count {int} -- number of barcodes to create in the group

        Returns:
            BarcodeGroup -- the barcode group created
        """
        next_values = self.__get_next_values(self.sequence_name, count)
        barcodes = [self.formatter().barcode(next_value) for next_value in next_values]
        return self.__create_barcode_group(barcodes)

    def create_children_barcode_group(self, parent_barcode: str, count: int) -> BarcodesGroup:
        """Creates a new barcode group and the associated barcodes.

        Arguments:
            count {int} -- number of barcodes to create in the group

        Returns:
            BarcodeGroup -- the barcode group created
        """
        barcodes = self.create_child_barcodes(parent_barcode, count)
        return self.__create_barcode_group(barcodes)

    def create_barcode(self) -> Barcode:
        """Generate and store a barcode using the Heron formatter.

        Returns:
            str -- the generated barcode in the Heron format
        """
        logger.debug(f"Calling create_barcode for sequence name {self.sequence_name}")
        try:
            next_value = self.__get_next_value(self.sequence_name)
            barcode = self.__build_barcode(
                prefix=self.prefix, barcode=self.formatter().barcode(next_value), barcodes_group=None
            )

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

    def __build_barcode(self, prefix: str, barcode: str, barcodes_group: Optional[BarcodesGroup]) -> Barcode:
        """Creates a new instance for Barcode with the arguments received, relating them to a
        BarcodeGroup if provided, and setting a created_at timestamp.

        Arguments:
            prefix : str - prefix of the barcode
            barcode : str - string with the barcode value
            barcodes_group : Optional[BarcodesGroup] - instance of BarcodesGroup or None if not needed

        Returns:
            Barcode instance with the arguments set and a created_at timestamp attached
        """
        return Barcode(
            prefix=prefix,
            barcode=barcode,
            created_at=datetime.now(),
            barcodes_group=barcodes_group,
        )

    def __create_barcode_group(self, barcodes: List[str]) -> BarcodesGroup:
        """Creates a new barcode group and the associated barcodes.

        Arguments:
            count {int} -- number of barcodes to create in the group

        Returns:
            BarcodeGroup -- the barcode group created
        """
        try:
            barcodes_group = self.__build_barcodes_group()
            db.session.add(barcodes_group)

            barcodes_instances = [
                self.__build_barcode(prefix=self.prefix, barcode=barcode, barcodes_group=barcodes_group)
                for barcode in barcodes
            ]
            db.session.add_all(barcodes_instances)

            db.session.commit()

            return barcodes_group
        except Exception as e:
            db.session.rollback()
            raise e

    def __build_barcodes_group(self) -> BarcodesGroup:
        """Creates a new instance for BarcodesGroup, and sets
         a created_at timestamp.

        Arguments: None

        Returns:
            BarcodesGroup instance with a created_at timestamp attached
        """
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

    # Child barcode operations
    def is_valid_parent_barcode(self, barcode: str) -> Boolean:
        """Boolean function that identifies if a barcode can act as a parent barcode.
        It checks that the barcode matches the format of the regexp declared in the
        #extract_barcode_parent_information method.

        Arguments:
            barcode - str : Barcode that we want to check if it is valid parent

        Returns:
            bool indicating if the barcode was a valid parent
        """
        return not self.extract_barcode_parent_information(barcode) is None

    def extract_barcode_parent_information(self, barcode: str) -> Optional[BarcodeParentInfoType]:
        """Extracts the parent and child information from a barcode string by following the regexp
        defined. If the input does not match it will return None.
        Eg:  barcode HT-1111-23 it will extract parent: HT-1111 and child: 23
             barcode HT-1111 it will extract parent: HT-1111 and child: None

        Arguments:
            barcode - str : Barcode string where we want to extract data from

        Returns:
            BarcodeParentInfoType object with the fields parent_barcode and child, or
            None if the barcode string from input did not match the regexp.
        """
        pattern = re.compile(f"^(?P<parent_barcode>{self.prefix}-\\d+)(?:-(?P<child>\\d+))?$")
        found = pattern.search(barcode)
        if not found:
            return None
        return {
            "parent_barcode": found.group("parent_barcode"),
            "child": found.group("child"),
        }

    def validate_prefix_for_child_creation(self) -> None:
        """Validates if self.prefix is declared as children creation enabled and if not
        it will raise an exception.

        Returns:
            None if prefix has children creation enabled
            Raise InvalidPrefixForChildrenCreation if not enabled
        """
        if not cast(PrefixesType, self.prefix_item)["enableChildrenCreation"]:
            raise InvalidPrefixForChildrenCreation()

    def validate_barcode_parent_information(self, info: Optional[BarcodeParentInfoType]) -> None:
        """Validates if barcode has all the correct information to generate children barcodes.
        It will check that:
          - The barcode was correctly parsed in the object as input, otherwise it will raise
          InvalidParentBarcode
          - The parent barcode, if is a child barcode, it was generated as a child before by Baracoda
          otherwise it will be rejected and raise InvalidParentBarcode

        Returns:
            None if checks were ok
            Raise InvalidParentBarcode if not correct
        """
        if not info:
            raise InvalidParentBarcode("The barcode provided is not valid for generating child barcodes")

        barcode_record = db.session.query(ChildBarcode).filter_by(barcode=info["parent_barcode"]).first()

        if barcode_record is None:
            if info["child"]:
                raise InvalidParentBarcode("The barcode provided is an impostor barcode. It has no parent.")
            return

        if info["child"]:
            child_position = int(info["child"])
            if barcode_record.child_count < child_position:
                raise InvalidParentBarcode(
                    "The barcode provided is an impostor barcode. Its parent has not generated this position yet."
                )

    def create_child_barcodes(self, parent_barcode: str, count: int) -> List[str]:
        """Retrieve the next child barcodes for a given barcode

        Returns:
            [str] -- The generated child barcodes
        """
        try:
            # Check barcode exists
            barcode_record = db.session.query(ChildBarcode).with_for_update().filter_by(barcode=parent_barcode).first()

            # If no record, then create one
            if barcode_record is None:
                old_count = 0
                barcode_record = ChildBarcode(barcode=parent_barcode, child_count=count)
                db.session.add(barcode_record)
            else:
                old_count = barcode_record.child_count
                barcode_record.child_count = old_count + count

            db.session.commit()

            # We want the new count to start at the next number
            new_count = old_count + 1

            # Format child barcodes
            child_barcodes = []
            for pos in range(new_count, barcode_record.child_count + 1):
                barcode = self.formatter().child_barcode(parent_barcode, pos)
                child_barcodes.append(barcode)

            return child_barcodes
        except Exception as e:
            db.session.rollback()
            raise e
