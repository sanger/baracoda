from sqlalchemy import Column, Integer, String, DateTime, Sequence
from sqlalchemy.orm import relationship

from baracoda.orm.base import Base


class BarcodesGroup(Base):
    __tablename__ = "barcodes_groups"

    id = Column(Integer, Sequence("barcodes_groups_id_seq"), primary_key=True)
    created_at = Column(DateTime)
    barcodes = relationship("Barcode", back_populates="barcodes_group")

    def __repr__(self):
        return "<BarcodesGroup(id='%s', barcodesCount='%s', created_at='%s')>" % (
            self.id,
            len(self.barcodes),
            self.created_at,
        )

    def to_hash(self):
        return {
            "barcode_group": {
                "id": self.id,
                "barcodes": [barcode.barcode for barcode in self.barcodes],
            }
        }
