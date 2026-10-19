__all__ = [
    "RandomStateType",
    "StrictRandomStateType",
]

from typing import Annotated, Any

from numpy.random import RandomState
from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, PydanticCustomError, core_schema

from ..utils import before_validator_decorator, isinstance_func


class StrictRandomStateType(RandomState):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        return core_schema.no_info_plain_validator_function(
            isinstance_func(RandomState)
        )


@before_validator_decorator
def coerce(value: Any) -> RandomState:
    if isinstance(value, RandomState):
        return value
    
    try:
        return RandomState(value)
    except Exception as exc:
        raise PydanticCustomError(
            "validation_error", 
            f"Failed to coerce value to RandomState: {exc}"
        ) from exc


type RandomStateType = Annotated[StrictRandomStateType, coerce]
