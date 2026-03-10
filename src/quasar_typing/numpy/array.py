from numpy import ndarray, issubdtype
from numpy.typing import NDArray
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class Array_(NDArray):
    @classmethod
    def _validate(cls, value: object) -> NDArray:
        if not isinstance(value, ndarray):
            msg = f'Expected numpy array, got {type(value)}'
            raise PydanticCustomError('validation_error', msg)
        return value
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)
    
    @classmethod
    def __class_getitem__(cls, specs) -> type['Array_']:
        if not isinstance(specs, tuple):
            specs = (specs,)

        doc = specs[0]
        dtype = specs[1]
        ndim = specs[2] if len(specs) > 2 else None        

        class TypedArray_(Array_):
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
            def __get_pydantic_core_schema__(cls, source_type, handler):
                return no_info_plain_validator_function(cls._validate)
            
        TypedArray_.__doc__ = doc
            
        return TypedArray_