from typing import List, Union, TypedDict, Type
from baracoda.formats.heron import HeronCogUkIdFormatter
from baracoda.formats.generic import GenericBarcodeFormatter
from baracoda.formats.sequencescape import Sequencescape22Formatter

FormatterClassType = Union[Type[HeronCogUkIdFormatter], Type[GenericBarcodeFormatter], Type[Sequencescape22Formatter]]

PrefixesType = TypedDict(
    "PrefixesType",
    {"prefix": str, "sequence_name": str, "formatter_class": FormatterClassType, "enableChildrenCreation": bool},
)

BarcodeParentInfoType = TypedDict(
    "BarcodeParentInfoType",
    {"parent_barcode": str, "child": str, "suffix": str},
)


FormatterInterfaceType = List[PrefixesType]
