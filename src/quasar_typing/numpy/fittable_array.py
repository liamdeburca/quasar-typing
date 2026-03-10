from numpy import ndarray, issubdtype, isfinite, invert
from numpy.typing import NDArray
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class FittableArray_(NDArray):
    @classmethod
    def _validate(cls, value: object) -> NDArray:
        if not isinstance(value, ndarray):
            msg = f'Expected numpy array, got {type(value)}'
            raise PydanticCustomError('validation_error', msg)
        
        if not (mask := isfinite(value)).all():
            non_finite_count: int = invert(mask).sum()
            msg = "Expected numpy array with finite values, " \
                "got array with {} non-finite values".format(
                    non_finite_count,
                )
            raise PydanticCustomError('validation_error', msg)
        
        if not value.size > 0:
            msg = "Expected numpy array with at least one element, "\
                "got an empty array"
            raise PydanticCustomError('validation_error', msg)
        
        return value
    
    @classmethod
    def __pydantic_get_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)
    
    @classmethod
    def __class_getitem__(cls, specs) -> type['FittableArray_']:
        if not isinstance(specs, tuple):
            specs = (specs,)

        dtype = specs[0]
        ndim = specs[1] if len(specs) > 1 else None        

        class TypedFittableArray_(FittableArray_):
            @classmethod
            def _validate(cls, value: object) -> NDArray:
                array = super()._validate(value)

                if dtype is not None and not issubdtype(array.dtype, dtype):
                    msg = f'Expected numpy array of dtype {dtype}, " \
                        "got {array.dtype}'
                    raise PydanticCustomError('validation_error', msg)

                if ndim is not None and array.ndim != ndim:
                    msg = f'Expected numpy array of ndim {ndim}, " \
                        "got {array.ndim}'
                    raise PydanticCustomError('validation_error', msg)

                return array
            
            @classmethod
            def __pydantic_get_core_schema__(cls, source_type, handler):
                return no_info_plain_validator_function(cls._validate)
            
        return TypedFittableArray_