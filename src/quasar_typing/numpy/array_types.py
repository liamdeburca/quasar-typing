"""Type aliases for numpy arrays and related types."""

from typing import Annotated

from numpy import bool_, float64, int64

from quasar_typing.astropy.units import QuantityType

from . import validators
from .array import (
    BoolArray,
    FloatingArray,
    IntegerArray,
)

# Float Arrays

type FloatArray = FloatingArray[tuple, float64]
type FloatVector = FloatingArray[tuple[int], float64]
type FloatMatrix = FloatingArray[tuple[int, int], float64]
type FloatCube = FloatingArray[tuple[int, int, int], float64]

type CoordsTuple = Annotated[
    tuple[
        FloatVector | QuantityType, 
        FloatVector | QuantityType, 
        FloatVector | QuantityType,
    ],
    validators.all_same_shape,
]

type SpectrumCoordsTuple = Annotated[
    tuple[FloatVector, FloatVector, FloatVector],
    validators.all_same_shape,
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
    validators.has_elements,
    validators.only_finites,
]
type FittableFloatVector = Annotated[
    FloatVector,
    validators.has_elements,
    validators.only_finites,
]
type FittableFloatMatrix = Annotated[
    FloatMatrix,
    validators.has_elements,
    validators.only_finites,
]
type FittableFloatCube = Annotated[
    FloatCube,
    validators.has_elements,
    validators.only_finites,
]

type FittableCoordsTuple = Annotated[
    tuple[FittableFloatArray, FittableFloatArray, FittableFloatArray],
    validators.all_same_shape,
]

# Sorted Arrays

type SortedFloatVector = Annotated[
    FloatVector,
    validators.only_finites,
    validators.has_elements,
    validators.is_sorted,
]
type SortedIntVector = Annotated[
    IntVector,
    validators.only_finites,
    validators.has_elements,
    validators.is_sorted,
]
