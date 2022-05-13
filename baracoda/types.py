from typing import List, Union, TypedDict, Type
from baracoda.formats import HeronCogUkIdFormatter, GenericBarcodeFormatter

FormatterClassType = Union[Type[HeronCogUkIdFormatter], Type[GenericBarcodeFormatter]]

PrefixesType = TypedDict(
    "PrefixesType",
    {"prefix": str, "sequence_name": str, "formatter_class": FormatterClassType, "enableChildrenCreation": bool},
)

BarcodeParentInfoType = TypedDict(
    "BarcodeParentInfoType",
    {"parent_barcode": str, "child": str},
)


FormatterInterfaceType = List[PrefixesType]
