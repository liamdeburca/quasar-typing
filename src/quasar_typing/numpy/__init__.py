__all__ = [
    "Array",
    "BoolArray",
    "BoolCube",
    "BoolMatrix",
    "BoolVector",
    "CoordsTuple",
    "FittableCoordsTuple",
    "FittableFloatArray",
    "FittableFloatCube",
    "FittableFloatMatrix",
    "FittableFloatVector",
    "FloatArray",
    "FloatCube",
    "FloatMatrix",
    "FloatVector",
    "IntArray",
    "IntCube",
    "IntMatrix",
    "IntVector",
    "RandomStateType",
    "SortedFloatVector",
    "SortedIntVector",
    "SpectrumCoordsTuple",
    "StrictRandomStateType",
]
from typing import Annotated

from numpy import bool_, float64, int64

from quasar_typing.astropy import QuantityType

from .array import (
    Array,
    BoolArray,
    FloatingArray,
    IntegerArray,
    all_same_shape,
    has_elements,
    is_sorted,
    only_finites,
)
from .random import RandomStateType, StrictRandomStateType

type CoordsTuple = Annotated[
    tuple[
        FloatVector | QuantityType, 
        FloatVector | QuantityType, 
        FloatVector | QuantityType,
    ],
    all_same_shape,
]

# Float Arrays

type FloatArray = FloatingArray[tuple, float64]
type FloatVector = FloatingArray[tuple[int], float64]
type FloatMatrix = FloatingArray[tuple[int, int], float64]
type FloatCube = FloatingArray[tuple[int, int, int], float64]

type SpectrumCoordsTuple = Annotated[
    tuple[FloatVector, FloatVector, FloatVector],
    all_same_shape,
]

# Int Arrays

type IntArray = IntegerArray[tuple, int64]
type IntVector = IntegerArray[tuple[int], int64]
type IntMatrix = IntegerArray[tuple[int, int], int64]
type IntCube = IntegerArray[tuple[int, int, int], int64]

# Bool Arrays

type BoolVector = BoolArray[tuple[int], bool_]
type BoolMatrix = BoolArray[tuple[int, int], bool_]
type BoolCube = BoolArray[tuple[int, int, int], bool_]

# Fittable Float Arrays

type FittableFloatArray = Annotated[
    FloatArray,
    has_elements,
    only_finites,
]
type FittableFloatVector = Annotated[
    FloatVector,
    has_elements,
    only_finites,
]
type FittableFloatMatrix = Annotated[
    FloatMatrix,
    has_elements,
    only_finites,
]
type FittableFloatCube = Annotated[
    FloatCube,
    has_elements,
    only_finites,
]

type FittableCoordsTuple = Annotated[
    tuple[FittableFloatArray, FittableFloatArray, FittableFloatArray],
    all_same_shape,
]

# Sorted Arrays

type SortedFloatVector = Annotated[
    FloatVector,
    only_finites,
    has_elements,
    is_sorted,
]
type SortedIntVector = Annotated[
    IntVector,
    only_finites,
    has_elements,
    is_sorted,
]