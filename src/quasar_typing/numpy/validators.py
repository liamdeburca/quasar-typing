
from numpy import ndarray

from ..utils import after_validator_decorator


@after_validator_decorator
def only_finites(value: ndarray) -> ndarray:
    from numpy import isfinite
    from pydantic_core import PydanticCustomError
    mask = isfinite(value)
    n = mask.sum()
    if n != value.size:
        raise PydanticCustomError(
            "validation_error",
            f"Array contains {value.size - n} non-finite values"
        )
    return value


@after_validator_decorator
def has_elements(value: ndarray) -> ndarray:
    from pydantic_core import PydanticCustomError
    if value.size == 0:
        raise PydanticCustomError(
            "validation_error",
            "Array must have at least one element"
        )
    return value

@after_validator_decorator
def is_sorted(value: ndarray) -> ndarray:
    from pydantic_core import PydanticCustomError
    if not (value[...,:-1] <= value[...,1:]).all():
        raise PydanticCustomError(
            "validation_error",
            "Array is not sorted along its last axis"
        )
    return value

@after_validator_decorator
def all_same_shape(value: tuple[ndarray, ...]) -> tuple[ndarray, ...]:
    from pydantic_core import PydanticCustomError
    shapes = [arr.shape for arr in value]
    if not all(shape == shapes[0] for shape in shapes[1:]):
        raise PydanticCustomError(
            "validation_error",
            f"All arrays must have the same shape, got: {shapes}"
        )
    return value