__all__ = [
    'FloatArray', 'FloatVector', 'FloatMatrix', 'FloatCube',
    'IntArray', 'IntVector', 'IntMatrix', 'IntCube',
    'BoolArray', 'BoolVector', 'BoolMatrix', 'BoolCube',
    'FittableFloatArray', 'FittableFloatVector', 'FittableFloatMatrix', 
    'FittableFloatCube',
    'FittableCoordsTuple',
    'SortedFloatVector',
    'RandomState_',
]

from numpy import floating, integer, bool_

from .array import Array_
from .fittable_array import FittableArray_
from .fittable_coords_tuple import FittableCoordsTuple
from .sorted_array import SortedArray_
from .random_state import RandomState_

# Float Arrays

_doc: str = "{}numpy.array of floats"
FloatArray  = Array_[_doc.format(""),    floating]
FloatVector = Array_[_doc.format("1D "), floating, 1]
FloatMatrix = Array_[_doc.format("2D "), floating, 2]
FloatCube   = Array_[_doc.format("3D "), floating, 3]

# Int Arrays

_doc: str = "{}numpy.array of integers"
IntArray  = Array_[_doc.format(""),    integer]
IntVector = Array_[_doc.format("1D "), integer, 1]
IntMatrix = Array_[_doc.format("2D "), integer, 2]
IntCube   = Array_[_doc.format("3D "), integer, 3]

# Bool Arrays

_doc: str = "{}numpy.array of booleans"
BoolArray  = Array_[_doc.format(""),    bool_]
BoolVector = Array_[_doc.format("1D "), bool_, 1]
BoolMatrix = Array_[_doc.format("2D "), bool_, 2]
BoolCube   = Array_[_doc.format("3D "), bool_, 3]

# Fittable Float Arrays

_doc: str = "non-empty {}numpy.array of purely floats"
FittableFloatArray  = FittableArray_[_doc.format(""),    floating]
FittableFloatVector = FittableArray_[_doc.format("1D "), floating, 1]
FittableFloatMatrix = FittableArray_[_doc.format("2D "), floating, 2]
FittableFloatCube   = FittableArray_[_doc.format("3D "), floating, 3]

# Sorted Arrays

_doc: str = "sorted 1D numpy.array of {}"
SortedFloatVector = SortedArray_[_doc.format("floats"),   floating]
SortedIntVector   = SortedArray_[_doc.format("integers"), integer]