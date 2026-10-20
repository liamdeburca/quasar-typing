import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter

_import_structure: dict[str, list[str]] = {
    "array": [
        "Array",
        "BoolArray",
        "FloatArray",
        "IntegerArray",
        "StrArray",
    ],
    "_types": [
        "FloatVector",
        "FloatMatrix",
        "FloatCube",
        "CoordsTuple",
        
        "IntArray",
        "IntVector",
        "IntMatrix",
        "IntCube",
        
        "BoolVector",
        "BoolMatrix",
        "BoolCube",


        "FittableFloatArray",
        "FittableFloatVector",
        "FittableFloatMatrix",
        "FittableFloatCube",
        "FittableCoordsTuple",
        "SpectrumCoordsTuple",

        "SortedFloatVector",
        "SortedIntVector",
    ],
}

if TYPE_CHECKING:
    from .array import (  # noqa: F401
        Array,
        BoolArray,
        FloatArray,
        IntegerArray,
        StrArray,
    )
    from .array_types import (  # noqa: F401
        BoolCube,
        BoolMatrix,
        BoolVector,
        CoordsTuple,
        FittableCoordsTuple,
        FittableFloatArray,
        FittableFloatCube,
        FittableFloatMatrix,
        FittableFloatVector,
        FloatCube,
        FloatMatrix,
        FloatVector,
        IntArray,
        IntCube,
        IntMatrix,
        IntVector,
        SortedFloatVector,
        SortedIntVector,
        SpectrumCoordsTuple,
    )
else:
    sys.modules[__name__] = LazyImporter(
        __name__,
        __file__,
        _import_structure,
    )
