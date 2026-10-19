__all__ = ["CoordsTuple"]

from typing import ClassVar, TypeVar

from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_after_validator_function

from ._array import Array_

T = TypeVar("T", bound=Array_)


class CoordsTuple[T](tuple[T, T, T]):
    """
    3-tuple of equally-sized 1d numpy arrays
    """
    _element_type: ClassVar[type] = Array_ 

    @classmethod
    def _validate_same_shape(cls, value: tuple[T, T, T]) -> tuple[T, T, T]:
        arr1, arr2, arr3 = value
        if not (arr1.shape == arr2.shape and arr2.shape == arr3.shape):
            raise PydanticCustomError(
                "validation_error",
                "Expected numpy arrays of the same shape, got arrays of "
                f"shapes {arr1.shape}, {arr2.shape}, and {arr3.shape}",
            )
        return value

    # @classmethod
    # def _validate(cls, value: Any) -> tuple[T, T, T]:
    #     if not isinstance(value, tuple):
    #         try:
    #             value = tuple(value)
    #         except Exception as exc:
    #             raise PydanticCustomError(
    #                 "validation_error",
    #                 f"Expected a tuple of length 3, got value that cannot be converted to tuple: {value}",
    #             ) from exc
    #     if len(value) != 3:
    #         raise PydanticCustomError(
    #             "validation_error",
    #             f"Expected a tuple of length 3, got length {len(value)}",
    #         )

    #     vs = []
    #     for i, v in enumerate(value):
    #         vs.append(cls._element_type._validate(v))

    #     value = tuple(vs)
    
    #     return cls._validate_same_shape(value)

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        element_type = cls._element_type
        tuple_type = tuple[element_type, element_type, element_type]
        tuple_schema = handler.generate_schema(tuple_type)

        return no_info_after_validator_function(
            cls._validate_same_shape,
            tuple_schema,
        )

    @classmethod
    def __class_getitem__(cls, subtype: type[T]) -> type["CoordsTuple[T]"]:
        class TypedCoordsTuple(cls):
            _element_type: ClassVar[type] = subtype
        return TypedCoordsTuple
