from collections.abc import Callable
from typing import Any, TypeVar

from pydantic import AfterValidator, BeforeValidator
from pydantic_core import PydanticCustomError

T = TypeVar("T", bound=type[Any])

def before_validator_decorator(func) -> BeforeValidator:
    return BeforeValidator(func)


def after_validator_decorator(func) -> AfterValidator:
    return AfterValidator(func)


def simple_coersion_validator(t: type) -> BeforeValidator:
    def func(value: Any) -> Any:
        try:
            return t(value)
        except Exception as exc:
            raise PydanticCustomError(
                "validation_error",
                f"Could not coerce value of type {type(value).__name__} to "
                f"{t.__name__}"
            ) from exc
    return BeforeValidator(func)


def isinstance_func(t: type) -> Callable[[Any], Any]:
    def func(value: Any) -> Any:
        if not isinstance(value, t):
            raise PydanticCustomError(
                "validation_error",
                f"Expected an instance of {t.__name__}, "
                f"got {type(value).__name__}"
            )
        return value
    return func


def isinstance_validator(t: type) -> AfterValidator:
    return AfterValidator(isinstance_func(t))