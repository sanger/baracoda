from sqlalchemy import Column, Integer, String
from baracoda.orm.base import Base


class ChildBarcode(Base):
    """Class that will define the ORM mapping with the database. It will
    store a list of all parent barcodes with an index of the last created
    child for the parent for each entry.
    """

    __tablename__ = "child_barcode_counter"

    barcode = Column(String(50), nullable=False, primary_key=True)
    child_count = Column(Integer, nullable=True)

    def __repr__(self):
        return "<ChildBarcode(barcode='%s', child_count='%s')>" % (
            self.barcode,
            self.child_count,
        )

    def to_dict(self):
        return {"barcode": self.barcode, "child_count": self.child_count}
