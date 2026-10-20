import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter

_import_structure: dict[str, list[str]] = {
    "coordinates": [
        "SkyCoordType",
    ],
    "fits": [
        "BinTableHDUType",
        "HDUListType",
        "ImageHDUType",
        "PrimaryHDUType"
    ],
    "modeling": [
        "CompoundModelType", 
        "Fittable1DModelType", 
        "ModelType", 
        "ParameterType",
    ],
    "table": [
        "ColumnType",
        "QTableType",
        "RowType",
        "TableType",
    ],
    "units": [
        "CompositeUnitType", "QuantityType", "UnitType"
    ]
}

if TYPE_CHECKING:
    from .coordinates import SkyCoordType  # noqa: F401
    from .fits import (  # noqa: F401
        BinTableHDUType,
        HDUListType,
        ImageHDUType,
        PrimaryHDUType,
    )
    from .modeling import (  # noqa: F401
        CompoundModelType,
        Fittable1DModelType,
        ModelType,
        ParameterType,
    )
    from .table import ColumnType, QTableType, RowType, TableType  # noqa: F401
    from .units import CompositeUnitType, QuantityType, UnitType  # noqa: F401
else:
    sys.modules[__name__] = LazyImporter(
        __name__,
        __file__,
        _import_structure,
    )