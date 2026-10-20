from typing import Any, ClassVar

from numpy import bool_, floating, integer, ndarray, str_
from numpy.typing import DTypeLike


class Array(ndarray):
    _subdtype_of: ClassVar[DTypeLike | None] = None
    _shape: ClassVar[type] = tuple
    _dtype: ClassVar[DTypeLike | None] = None

    @classmethod
    def validate(cls, value: Any, source_type: Any = None) -> ndarray:
        from numpy import asarray, can_cast, issubdtype
        from pydantic import TypeAdapter
        from pydantic_core import PydanticCustomError

        try:
            value = asarray(value)
        except ValueError:
            raise PydanticCustomError(
                "validation_error",
                "Failed to coerce value to numpy array"
            )
        
        # Check if dtype coercion is safe and do it
        if cls._dtype is not None and value.dtype != cls._dtype:
            if not can_cast(value.dtype, cls._dtype):
                raise PydanticCustomError(
                    "validation_error",
                    f"Cannot safely coerce array (dtype={value.dtype}) "
                    f"to {cls._dtype}"
                )
            value = value.astype(cls._dtype, copy=False)

        # Check subdtype compatibility (after coercion if applicable)
        if cls._subdtype_of is not None \
            and not issubdtype(value.dtype, cls._subdtype_of):
            raise PydanticCustomError(
                "validation_error",
                f"Array (dtype={value.dtype}) must be of subdtype "
                f"{cls._subdtype_of}"
            )

        if cls._shape is not None:
            TypeAdapter(cls._shape).validate_python(value.shape)
        
        return value

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: Any,
    ):
        """Get the Pydantic core schema for validation."""
        from pydantic_core.core_schema import no_info_plain_validator_function
        return no_info_plain_validator_function(
            lambda v: cls.validate(v, source_type=source_type),
        )
    

    def __class_getitem__(cls, item) -> type["Array"]:
        from numpy import dtype, issubdtype

        if len(item) == 1:
            class TypedArray(cls):
                _shape = item[0]
        else:
            if not issubdtype(item[1], cls._subdtype_of):
                raise TypeError(
                    f"Array dtype {item[1]} is not a subdtype of "
                    f"{cls._subdtype_of}"
                )
            class TypedArray(cls):
                _shape = item[0]
                _dtype = dtype(item[1])

        return TypedArray

class FloatingArray(Array):
    _subdtype_of = floating

class IntegerArray(Array):
    _subdtype_of = integer

class BoolArray(Array):
    _subdtype_of = bool_

class StrArray(Array):
    _subdtype_of = str_