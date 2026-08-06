__all__ = [
    "RandomState_",
    "StrictRandomState_",
]

from typing import ClassVar, Literal

from numpy.random import RandomState
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function


class RandomState_(RandomState):
    """
    numpy.random.RandomState

    Wrapper that automatically coerces input (int or array) to
    RandomState, enabling flexible initialization from seeds.
    """
    _coerce: ClassVar[Literal[True]] = True

    @classmethod
    def _validate(cls, value: object) -> RandomState:
        if not isinstance(value, RandomState):
            if cls._coerce:
                try:
                    value = RandomState(value)
                except Exception as e:
                    msg = "Tried to coerce value of type "\
                        f"{type(value).__name__} to {cls.__name__}, "\
                        f"but got error: {e}"
                    raise PydanticCustomError("validation_error", msg)
            else:
                msg = "Expected numpy.random.RandomState, "\
                    f"got {type(value).__name__}"
                raise PydanticCustomError("validation_error", msg)
        return value

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)


class StrictRandomState_(RandomState_):
    """
    numpy.random.RandomState (strict validation, no coercion)

    Wrapper that requires input to already be a RandomState instance.
    Rejects non-RandomState values without coercion.
    """
    _coerce: ClassVar[Literal[False]] = False
