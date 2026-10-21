__all__ = ["PolynomialOrder", "WindowSize"]

from typing import Annotated

from pydantic import NonNegativeInt, PositiveInt
from pydantic_core import PydanticCustomError

from quasar_typing.utils import after_validator_decorator


@after_validator_decorator
def validate_is_odd(value: int) -> int:
    if value % 2 == 0:
        raise PydanticCustomError(
            "validation_error",
            "Value must be odd",
        )
    return value


type WindowSize = Annotated[PositiveInt, validate_is_odd]
type PolynomialOrder = NonNegativeInt