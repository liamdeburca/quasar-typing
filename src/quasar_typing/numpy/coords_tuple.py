__all__ = ['CoordsTuple']

from typing import TypeVar, get_args
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_after_validator_function

from .array import Array_

T = TypeVar('T', bound=Array_)
    
class CoordsTuple[T](tuple[T, T, T]):
    """
    3-tuple of equally-sized 1d numpy arrays
    """
    @classmethod
    def _validate_same_shape(cls, value: tuple[T, T, T]) -> tuple[T, T, T]:
        arr1, arr2, arr3 = value
        if not arr1.shape == arr2.shape == arr3.shape:
            raise PydanticCustomError(
                'validation_error', 
                "Expected numpy arrays of the same shape, got arrays of "
                f"shapes {arr1.shape}, {arr2.shape}, and {arr3.shape}"
            )
        return value
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        args = get_args(source_type)
        element_type = args[0] if args else Array_
        tuple_type = tuple[element_type, element_type, element_type]
        tuple_schema = handler.generate_schema(tuple_type)
        
        return no_info_after_validator_function(
            cls._validate_same_shape, 
            tuple_schema,
        )
    
    @classmethod
    def __class_getitem__(cls, subtype: type[T]) -> type['CoordsTuple[T]']:
        TypedCoordsTuple = super().__class_getitem__(subtype)
        return TypedCoordsTuple
        