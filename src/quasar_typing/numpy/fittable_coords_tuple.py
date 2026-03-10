from numpy import ndarray, isfinite, isdtype, invert, float64
from numpy.typing import NDArray
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class FittableCoordsTuple(tuple[NDArray[float64]]):
    """
    3-tuple of only-finite and non-empty 1D numpy arrays (float64)
    """
    @classmethod
    def _validate(cls, value: object) -> NDArray:
        if not isinstance(value, tuple):
            msg = f"Expected tuple, got {type(value)}"
            raise PydanticCustomError('validation_error', msg)
        
        if not len(value) == 3:
            msg = f"Expected tuple of length 3, got tuple of \
                length {len(value)}"
            raise PydanticCustomError('validation_error', msg)

        for i, arr in enumerate(value):
            if not isinstance(arr, ndarray):
                msg = f"Expected numpy array at index {i}, got {type(arr)}"
                raise PydanticCustomError('validation_error', msg)
            
            if not isdtype(arr.dtype, float64):
                msg = f"Expected numpy array of dtype float64 at index {i}, "\
                    f"got {arr.dtype}"
                raise PydanticCustomError('validation_error', msg)
            
            if not (mask := isfinite(arr)).all():
                non_finite_count: int = invert(mask).sum()
                msg = f"Expected numpy array with finite values at index {i}, \
                    got array with {non_finite_count} non-finite values"
                raise PydanticCustomError('validation_error', msg)
            
            if not arr.size > 0:
                msg = f"Expected numpy array with at least one element at \
                    index {i}, got an empty array"
                raise PydanticCustomError('validation_error', msg)
            
        sizes = [arr.size for arr in value]
        if not sizes[0] == sizes[1] == sizes[2]:
            msg = "Expected numpy arrays of the same size, got arrays of \
                sizes {}, {}, and {}".format(*sizes)
            raise PydanticCustomError('validation_error', msg)
        
        return value
    
    @classmethod
    def __pydantic_get_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)