from numpy import ndarray, issubdtype, isfinite, invert
from numpy.typing import NDArray
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class Array_(NDArray):
    """
    numpy.array
    """
    _dtype: type | None = None
    _ndim: int | None = None
    _check_finite: bool = False
    _check_has_elements: bool = False
    _check_is_sorted: bool = False

    @classmethod
    def _validate(cls, value: object) -> NDArray:
        msg = f"{cls.__doc__} // "
        if not isinstance(value, ndarray):
            msg += f"Expected numpy array, got {type(value)}"
            raise PydanticCustomError('validation_error', msg)
        if cls._dtype is not None and not issubdtype(value.dtype, cls._dtype):
            msg += f'Expected numpy array of dtype {cls._dtype}, \
                got {value.dtype}'
            raise PydanticCustomError('validation_error', msg)
        if cls._ndim is not None and value.ndim != cls._ndim:
            msg += f'Expected numpy array of ndim {cls._ndim}, \
                got {value.ndim}'
            raise PydanticCustomError('validation_error', msg)
        if cls._check_finite and not (mask := isfinite(value)).all():
            non_finite_count: int = invert(mask).sum()
            msg += f"Expected numpy array with finite values, \
                got array with {non_finite_count} non-finite values"
            raise PydanticCustomError('validation_error', msg)
        if cls._check_has_elements and not value.size > 0:
            msg += "Expected numpy array with at least one element, \
                got an empty array"
            raise PydanticCustomError('validation_error', msg)
        if cls._check_is_sorted and not (value[:-1] <= value[1:]).all():
            msg += "Expected numpy array sorted in non-descending order, \
                got unsorted array"
            raise PydanticCustomError('validation_error', msg)
        
        return value
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)
    
    @classmethod
    def __class_getitem__(cls, specs) -> type['Array_']:
        class TypedArray_(Array_):
            _dtype = specs[1]
            _ndim = specs[2]
            _check_finite = specs[3]
            _check_has_elements = specs[4]
            _check_is_sorted = specs[5]
        
        TypedArray_.__doc__ = specs[0]
            
        return TypedArray_