__all__ = [
    'FloatArray', 'FloatVector', 'FloatMatrix', 'FloatCube',
    'IntArray', 'IntVector', 'IntMatrix', 'IntCube',
    'BoolArray', 'BoolVector', 'BoolMatrix', 'BoolCube',
    'FittableFloatArray', 'FittableFloatVector', 'FittableFloatMatrix', 
    'FittableFloatCube',
    'SortedFloatVector', 'SortedIntVector',
    'SpectrumCoordsTuple', 'FittableCoordsTuple',
    'RandomState_',
]
from numpy import floating, integer, bool_
from .array import Array_
from .coords_tuple import CoordsTuple
from .random_state import RandomState_

# Float Arrays

_doc: str = "{}numpy.array of floats"
FloatArray  = Array_[_doc.format(""),    floating, None, False, False, False]
FloatVector = Array_[_doc.format("1D "), floating,    1, False, False, False]
FloatMatrix = Array_[_doc.format("2D "), floating,    2, False, False, False]
FloatCube   = Array_[_doc.format("3D "), floating,    3, False, False, False]

SpectrumCoordsTuple = CoordsTuple[FloatArray]

# Int Arrays

_doc: str = "{}numpy.array of integers"
IntArray  = Array_[_doc.format(""),    integer, None, False, False, False]
IntVector = Array_[_doc.format("1D "), integer,    1, False, False, False]
IntMatrix = Array_[_doc.format("2D "), integer,    2, False, False, False]
IntCube   = Array_[_doc.format("3D "), integer,    3, False, False, False]

# Bool Arrays

_doc: str = "{}numpy.array of booleans"
BoolArray  = Array_[_doc.format(""),    bool_, None, False, False, False]
BoolVector = Array_[_doc.format("1D "), bool_,    1, False, False, False]
BoolMatrix = Array_[_doc.format("2D "), bool_,    2, False, False, False]
BoolCube   = Array_[_doc.format("3D "), bool_,    3, False, False, False]

# Fittable Float Arrays

_doc: str = "non-empty {}numpy.array of purely floats"
FittableFloatArray  = Array_[_doc.format(""),    floating, None, True, True, False]
FittableFloatVector = Array_[_doc.format("1D "), floating,    1, True, True, False]
FittableFloatMatrix = Array_[_doc.format("2D "), floating,    2, True, True, False]
FittableFloatCube   = Array_[_doc.format("3D "), floating,    3, True, True, False]

FittableCoordsTuple = CoordsTuple[FittableFloatArray]

# Sorted Arrays

_doc: str = "sorted 1D numpy.array of {}"
SortedFloatVector = Array_[_doc.format("floats"),   floating, 1, True, True, True]
SortedIntVector   = Array_[_doc.format("integers"),  integer, 1, True, True, True]