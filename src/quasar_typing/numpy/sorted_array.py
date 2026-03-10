from numpy import ndarray, diff, issubdtype
from numpy.typing import NDArray
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class SortedArray_(NDArray):
    @classmethod
    def _validate(cls, value: object) -> NDArray:
        if not isinstance(value, ndarray):
            msg = f"Expected numpy array, got {type(value)}"
            raise PydanticCustomError('validation_error', msg)
        
        if not value.size > 0:
            msg = "Expected numpy array with at least one element, "\
                "got an empty array"
            raise PydanticCustomError('validation_error', msg)
        
        if not (diff(value) > 0).all():
            msg = "Expected sorted numpy array, got unsorted array"
            raise PydanticCustomError('validation_error', msg)
        
        return value
    
    @classmethod
    def __pydantic_get_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)
    
    @classmethod
    def __class_getitem__(cls, specs):
        doc: str = specs[0]
        dtype = specs[1]

        class TypedSortedArray_(SortedArray_):
            @classmethod
            def _validate(cls, value: object) -> NDArray:
                array = super()._validate(value)

                if dtype is not None and not issubdtype(array.dtype, dtype):
                    msg = f"Expected numpy array of dtype {dtype}, \
                        got {array.dtype}"
                    raise PydanticCustomError('validation_error', msg)

                return array
            
            @classmethod
            def __pydantic_get_core_schema__(cls, source_type, handler):
                return no_info_plain_validator_function(cls._validate)
            
        TypedSortedArray_.__doc__ = doc
            
        return TypedSortedArray_