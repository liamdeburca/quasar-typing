__all__ = [
    "BoolArray",
    "BoolCube",
    "BoolMatrix",
    "BoolVector",
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
    "RandomState_",
    "SortedFloatVector",
    "SortedIntVector",
    "SpectrumCoordsTuple",
    "StrictRandomState_",
]
from typing import ClassVar, Literal

from numpy import bool_, floating, integer

from .array import Array_
from .coords_tuple import CoordsTuple
from .random_state import RandomState_, StrictRandomState_

# Float Arrays

class FloatArray(Array_):
    """
    numpy.ndarray (floating-point dtype)

    Wrapper that automatically coerces input to floating-point arrays.
    """
    _coerce: ClassVar[Literal[True]] = True
    _dtype: ClassVar[type] = floating

class FloatVector(FloatArray):
    """
    numpy.ndarray (1D, floating-point dtype)

    1-dimensional array of floating-point values with automatic coercion.
    """
    _ndim: ClassVar[Literal[1]] = 1

class FloatMatrix(FloatArray):
    """
    numpy.ndarray (2D, floating-point dtype)

    2-dimensional array of floating-point values with automatic coercion.
    """
    _ndim: ClassVar[Literal[2]] = 2

class FloatCube(FloatArray):
    """
    numpy.ndarray (3D, floating-point dtype)

    3-dimensional array of floating-point values with automatic coercion.
    """
    _ndim: ClassVar[Literal[3]] = 3

class SpectrumCoordsTuple(CoordsTuple[FloatArray]):
    """
    tuple of numpy.ndarray (floating-point dtype)

    2-tuple of 1D floating-point arrays for spectrum coordinates (e.g.,
    wavelength and flux).
    """

# Int Arrays

class IntArray(Array_):
    """
    numpy.ndarray (integer dtype)

    Wrapper that automatically coerces input to integer arrays.
    """
    _coerce: ClassVar[Literal[True]] = True
    _dtype: ClassVar[type] = integer

class IntVector(IntArray):
    """
    numpy.ndarray (1D, integer dtype)

    1-dimensional array of integer values with automatic coercion.
    """
    _ndim: ClassVar[Literal[1]] = 1

class IntMatrix(IntArray):
    """
    numpy.ndarray (2D, integer dtype)

    2-dimensional array of integer values with automatic coercion.
    """
    _ndim: ClassVar[Literal[2]] = 2

class IntCube(IntArray):
    """
    numpy.ndarray (3D, integer dtype)

    3-dimensional array of integer values with automatic coercion.
    """
    _ndim: ClassVar[Literal[3]] = 3

# Bool Arrays

class BoolArray(Array_):
    """
    numpy.ndarray (boolean dtype)

    Wrapper that automatically coerces input to boolean arrays.
    """
    _coerce: ClassVar[Literal[True]] = True
    _dtype: ClassVar[type] = bool_

class BoolVector(BoolArray):
    """
    numpy.ndarray (1D, boolean dtype)

    1-dimensional array of boolean values with automatic coercion.
    """
    _ndim: ClassVar[Literal[1]] = 1

class BoolMatrix(BoolArray):
    """
    numpy.ndarray (2D, boolean dtype)

    2-dimensional array of boolean values with automatic coercion.
    """
    _ndim: ClassVar[Literal[2]] = 2

class BoolCube(BoolArray):
    """
    numpy.ndarray (3D, boolean dtype)

    3-dimensional array of boolean values with automatic coercion.
    """
    _ndim: ClassVar[Literal[3]] = 3

# Fittable Float Arrays

class FittableFloatArray(Array_):
    """
    numpy.ndarray (non-empty, floating-point dtype)

    Wrapper for non-empty floating-point arrays with automatic coercion.
    Validates that array is non-empty and all values are finite.
    """
    _coerce: ClassVar[Literal[True]] = True
    _dtype: ClassVar[type] = floating
    _check_finite: ClassVar[Literal[True]] = True
    _check_has_elements: ClassVar[Literal[True]] = True

class FittableFloatVector(FittableFloatArray):
    """
    numpy.ndarray (1D, non-empty, floating-point dtype)

    1D array of finite floating-point values for model fitting.
    """
    _ndim: ClassVar[Literal[1]] = 1

class FittableFloatMatrix(FittableFloatArray):
    """
    numpy.ndarray (2D, non-empty, floating-point dtype)

    2D array of finite floating-point values for model fitting.
    """
    _ndim: ClassVar[Literal[2]] = 2

class FittableFloatCube(FittableFloatArray):
    """
    numpy.ndarray (3D, non-empty, floating-point dtype)

    3D array of finite floating-point values for model fitting.
    """
    _ndim: ClassVar[Literal[3]] = 3

class FittableCoordsTuple(CoordsTuple[FittableFloatArray]):
    """
    tuple of numpy.ndarray (non-empty, floating-point dtype)

    2-tuple of non-empty finite floating-point arrays for spectrum
    coordinates.
    """

# Sorted Arrays

class SortedFloatVector(Array_):
    """
    numpy.ndarray (1D, sorted, floating-point dtype)

    1D sorted floating-point array with automatic coercion. Validates
    that values are sorted in non-descending order.
    """
    _coerce: ClassVar[Literal[True]] = True
    _dtype: ClassVar[type] = floating
    _ndim: ClassVar[Literal[1]] = 1
    _check_finite: ClassVar[Literal[True]] = True
    _check_has_elements: ClassVar[Literal[True]] = True
    _check_is_sorted: ClassVar[Literal[True]] = True

class SortedIntVector(SortedFloatVector):
    """
    numpy.ndarray (1D, sorted, integer dtype)

    1D sorted integer array. Inherits sorting validation from parent.
    """
    _dtype: ClassVar[type] = integer
    