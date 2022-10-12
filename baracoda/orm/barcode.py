from sqlalchemy import Column, DateTime, ForeignKey, Integer, Sequence, String
from sqlalchemy.orm import relationship

from baracoda.orm.base import Base


class Barcode(Base):
    __tablename__ = "barcodes"

    id = Column(Integer, Sequence("barcodes_id_seq"), primary_key=True)
    barcode = Column(String(255), nullable=False)
    prefix = Column(String(32), nullable=False)
    barcodes_group_id = Column(Integer, ForeignKey("barcodes_groups.id"), nullable=True, default=None, index=True)
    barcodes_group = relationship("BarcodesGroup", back_populates="barcodes")  # type: ignore

    created_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return "<Barcode(id='%s', barcode='%s', prefix='%s', created_at='%s', barcodes_group='%s')>" % (
            self.id,
            self.barcode,
            self.prefix,
            self.created_at,
            self.barcodes_group,
        )

    def to_dict(self):
        return {"barcode": self.barcode}
