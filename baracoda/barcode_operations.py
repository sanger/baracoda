import re
from datetime import datetime

from baracoda.db import get_db
from baracoda.exceptions import ValidationError
from baracoda.barcode_formats import HeronFormatter


class BarcodeOperations:
    def __init__(self, params):
        self.sequence_name = params["sequence_name"]
        self.prefix = params["prefix"]

        if "count" in params:
            self.count = params["count"]
        else:
            self.count = 1

        self.__check_prefix()
        self.__check_count()

        self.formatter = HeronFormatter({"prefix": self.prefix})

    def generate_barcodes(self):
        records = []
        db = get_db()
        with db.connection:
            with db.cursor as self.__cursor:
                for i in range(0, self.count):
                    next_value = self.__get_next_value(self.sequence_name)

                    hex_str = format(next_value, "X")
                    barcode = self.formatter.barcode(hex_str)

                    records.append({"barcode": barcode})
                self.__store_barcodes(records)
        return records

    def get_last_barcode(self, prefix: str):
        db = get_db()
        with db.connection:
            with db.cursor as self.__cursor:
                return self.__query_for_last_barcode()

    #
    # Validations private methods
    def __check_count(self):
        if not self.count > 0:
            raise ValidationError(
                "The number of elements in count has to be higher than 0"
            )

    def __check_prefix(self):
        if not self.__validate_prefix():
            raise ValidationError("The provided prefix is not allowed")

    def __validate_prefix(self):
        if not type(self.prefix) == str:
            return False
        expr = re.compile("^[A-Z0-9]{1,10}$")
        return bool(expr.match(self.prefix))

    # Database access private methods
    def __store_barcodes(self, records):
        timestamp = datetime.now()

        values = ",".join(
            map(
                lambda x: f"('{x['barcode']}', '{self.prefix}', '{timestamp}')",
                records,
            )
        )
        command_str = (
            f"INSERT INTO barcodes (barcode, prefix, created_at) VALUES {values};"
        )
        self.__cursor.execute(command_str)

    def __query_for_last_barcode(self):
        self.__cursor.execute(
            f"SELECT barcode FROM barcodes WHERE barcodes.prefix='{self.prefix}' ORDER BY created_at DESC LIMIT 1;"
        )
        result = self.__cursor.fetchone()
        return result[0]

    def __get_next_value(self, sequence_name: str):
        self.__cursor.execute(f"SELECT nextval('{sequence_name.lower()}');")
        result = self.__cursor.fetchone()

        return result[0]
