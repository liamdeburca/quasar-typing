from typing import Annotated

from .utils import after_validator_decorator


@after_validator_decorator
def is_increasing(
    v: tuple[float | None, float | None],
) -> tuple[float | None, float | None]:
    from pydantic_core import PydanticCustomError
    if None in v:
        return v

    if v[0] >= v[1]:
        raise PydanticCustomError(
            "validation_error",
            f"tuple values must be increasing, got {v}",
        )
    return v


@after_validator_decorator
def is_not_only_none(
    v: tuple[float | None, float | None],
) -> tuple[float | None, float | None]:
    from pydantic_core import PydanticCustomError
    if all(x is None for x in v):
        raise PydanticCustomError(
            "validation_error",
            f"tuple values cannot be only None, got {v}",
        )
    return v


type CoordBounds = Annotated[
    tuple[float, float],
    is_increasing,
]
type AstropyBounds = Annotated[
    tuple[float | None, float | None],
    is_not_only_none,
    is_increasing,
]
