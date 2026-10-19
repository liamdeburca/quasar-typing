from typing import Any, ClassVar

import numpy as np
from pydantic import GetCoreSchemaHandler, TypeAdapter
from pydantic_core import CoreSchema, PydanticCustomError, core_schema

from ..utils import after_validator_decorator


class Array(np.ndarray):
    _subdtype_of: ClassVar[np.dtype | None] = None
    _shape: ClassVar[type] = tuple
    _dtype: ClassVar[np.dtype | None] = None

    @classmethod
    def validate(cls, value: Any, source_type: Any = None) -> np.ndarray:
        try:
            value: np.ndarray = np.asarray(value)
        except ValueError:
            raise PydanticCustomError(
                "validation_error",
                "Failed to coerce value to numpy array"
            )
        
        # Check if dtype coercion is safe and do it
        if cls._dtype is not None and value.dtype != cls._dtype:
            if not np.can_cast(value.dtype, cls._dtype):
                raise PydanticCustomError(
                    "validation_error",
                    f"Cannot safely coerce array (dtype={value.dtype}) "
                    f"to {cls._dtype}"
                )
            value = value.astype(cls._dtype, copy=False)

        # Check subdtype compatibility (after coercion if applicable)
        if cls._subdtype_of is not None \
            and not np.issubdtype(value.dtype, cls._subdtype_of):
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
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        """Get the Pydantic core schema for validation."""
        return core_schema.no_info_plain_validator_function(
            lambda v: cls.validate(v, source_type=source_type),
        )
    

    def __class_getitem__(cls, item) -> type["Array"]:
        if len(item) == 1:
            class TypedArray(cls):
                _shape = item[0]
        else:
            if not np.issubdtype(item[1], cls._subdtype_of):
                raise TypeError(
                    f"Array dtype {item[1]} is not a subdtype of "
                    f"{cls._subdtype_of}"
                )
            class TypedArray(cls):
                _shape = item[0]
                _dtype = np.dtype(item[1])

        return TypedArray

class FloatingArray(Array):
    _subdtype_of = np.floating

class IntegerArray(Array):
    _subdtype_of = np.integer

class BoolArray(Array):
    _subdtype_of = np.bool_

class StrArray(Array):
    _subdtype_of = np.str_

### Validation functions

@after_validator_decorator
def only_finites(value: np.ndarray) -> np.ndarray:
    mask = np.isfinite(value)
    n = mask.sum()
    if n != value.size:
        raise PydanticCustomError(
            "validation_error",
            f"Array contains {value.size - n} non-finite values"
        )
    return value


@after_validator_decorator
def has_elements(value: np.ndarray) -> np.ndarray:
    if value.size == 0:
        raise PydanticCustomError(
            "validation_error",
            "Array must have at least one element"
        )
    return value

@after_validator_decorator
def is_sorted(value: np.ndarray) -> np.ndarray:
    if not (value[...,:-1] <= value[...,1:]).all():
        raise PydanticCustomError(
            "validation_error",
            "Array is not sorted along its last axis"
        )
    return value

@after_validator_decorator
def all_same_shape(value: tuple[np.ndarray, ...]) -> tuple[np.ndarray, ...]:
    shapes = [arr.shape for arr in value]
    if not all(shape == shapes[0] for shape in shapes[1:]):
        raise PydanticCustomError(
            "validation_error",
            f"All arrays must have the same shape, got: {shapes}"
        )
    return value