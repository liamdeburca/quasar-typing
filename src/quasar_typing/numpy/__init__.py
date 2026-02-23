__all__ = [
    'FloatArray', 'FloatVector', 'FloatMatrix', 'FloatCube',
    'IntArray', 'IntVector', 'IntMatrix', 'IntCube',
    'BoolArray', 'BoolVector', 'BoolMatrix', 'BoolCube',
    'FittableFloatArray', 'FittableFloatVector', 'FittableFloatMatrix', 
    'FittableFloatCube',
    'FittableCoordsTuple'
    'SortedFloatVector',
]

from numpy import floating, integer, bool_
from .array import Array_
from .fittable_array import FittableArray_
from .sorted_array import SortedArray_
from .random_state import RandomState_

FloatArray  = Array_[floating]
FloatVector = Array_[floating, 1]
FloatMatrix = Array_[floating, 2]
FloatCube   = Array_[floating, 3]

IntArray  = Array_[integer]
IntVector = Array_[integer, 1]
IntMatrix = Array_[integer, 2]
IntCube   = Array_[integer, 3]

BoolArray  = Array_[bool_]
BoolVector = Array_[bool_, 1]
BoolMatrix = Array_[bool_, 2]
BoolCube   = Array_[bool_, 3]

FittableFloatArray = FittableArray_[floating]
FittableFloatVector = FittableArray_[floating, 1]
FittableFloatMatrix = FittableArray_[floating, 2]
FittableFloatCube = FittableArray_[floating, 3]

FittableCoordsTuple = tuple[FittableFloatVector, 
                            FittableFloatVector, 
                            FittableFloatVector]

SortedFloatVector = SortedArray_[floating]