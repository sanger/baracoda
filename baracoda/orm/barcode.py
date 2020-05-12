from sqlalchemy import Column, Integer, String, DateTime, Sequence, ForeignKey
from sqlalchemy.orm import relationship

from baracoda.orm.base import Base


class Barcode(Base):
    __tablename__ = "barcodes"

    id = Column(Integer, Sequence("barcodes_id_seq"), primary_key=True)
    barcode = Column(String(255))
    prefix = Column(String(32))
    barcodes_group_id = Column(Integer, ForeignKey("barcodes_groups.id"))
    barcodes_group = relationship("BarcodesGroup", back_populates="barcodes")

    created_at = Column(DateTime)

    def __repr__(self):
        return "<Barcode(id='%s', barcode='%s', prefix='%s', created_at='%s')>" % (
            self.id,
            self.barcode,
            self.prefix,
            self.created_at,
        )

    def to_hash(self):
        return {"barcode": self.barcode}
