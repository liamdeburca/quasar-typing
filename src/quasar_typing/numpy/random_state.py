from numpy.random import RandomState
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class RandomState_(RandomState):
    """
    numpy.random.RandomState
    """
    @classmethod
    def _validate(cls, value: object) -> RandomState:
        if not isinstance(value, RandomState):
            try:
                value = RandomState(value)
            except Exception as e:
                msg = f"Tried to coerce value of type {type(value).__name__} " \
                    f"to {cls.__name__}, but got error: {e}"
                raise PydanticCustomError('validation_error', msg)
        return value
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)