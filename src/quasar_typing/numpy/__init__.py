import sys
from importlib import import_module
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter

import_module("numpy")

_import_structure: dict[str, list[str]] = {
    "array": [
        "Array",
        "BoolArray",
        "FloatingArray",
        "IntegerArray",
        "StrArray",
    ],
    "array_types": [
        "FloatArray",
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
    "random": [
        "RandomStateType",
        "StrictRandomStateType",
    ]
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
    from .random import (  # noqa: F401
        RandomStateType,
        StrictRandomStateType,
    )
else:
    sys.modules[__name__] = LazyImporter(
        __name__,
        __file__,
        _import_structure,
    )
