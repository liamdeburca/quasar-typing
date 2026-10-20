from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T", bound=type[Any])

def before_validator_decorator(func):
    from pydantic import BeforeValidator
    return BeforeValidator(func)


def after_validator_decorator(func):
    from pydantic import AfterValidator
    return AfterValidator(func)


def simple_coersion_validator(t: type):
    from pydantic_core import PydanticCustomError
    def func(value: Any) -> Any:
        try:
            return t(value)
        except Exception as exc:
            raise PydanticCustomError(
                "validation_error",
                f"Could not coerce value of type {type(value).__name__} to "
                f"{t.__name__}"
            ) from exc
    return before_validator_decorator(func)


def isinstance_func(t: type) -> Callable[[Any], Any]:
    from pydantic_core import PydanticCustomError
    def func(value: Any) -> Any:
        if not isinstance(value, t):
            raise PydanticCustomError(
                "validation_error",
                f"Expected an instance of {t.__name__}, "
                f"got {type(value).__name__}"
            )
        return value
    return func


def isinstance_validator(t: type):
    return after_validator_decorator(isinstance_func(t))