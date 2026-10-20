__all__ = [
    "RandomStateType",
    "StrictRandomStateType",
]

from typing import Annotated, Any

from numpy.random.mtrand import RandomState

from ..utils import before_validator_decorator, isinstance_func


class StrictRandomStateType(RandomState):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: Any,
    ):
        from pydantic_core.core_schema import no_info_plain_validator_function
        return no_info_plain_validator_function(
            isinstance_func(RandomState)
        )


@before_validator_decorator
def coerce(value: Any) -> RandomState:
    from pydantic_core import PydanticCustomError
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
