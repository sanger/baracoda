from sqlalchemy import Column, Integer, String
from baracoda.orm.base import Base


class BarcodeSequence(Base):
    """ORM model for barcode_sequence_counters table.

    Replaces PostgreSQL SEQUENCE objects with a MySQL-compatible
    counter table. Each row represents one named sequence.
    """

    __tablename__ = "barcode_sequence_counters"

    sequence_name = Column(String(50), nullable=False, primary_key=True)
    current_value = Column(Integer, nullable=False)

    def __repr__(self):
        return "<BarcodeSequence(sequence_name='%s', current_value='%s')>" % (
            self.sequence_name,
            self.current_value,
        )

    def to_dict(self):
        return {"sequence_name": self.sequence_name, "current_value": self.current_value}
