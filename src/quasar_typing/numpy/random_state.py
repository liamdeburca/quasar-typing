from numpy.random import RandomState
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class RandomState_(RandomState):
    @classmethod
    def _validate(cls, value: object) -> RandomState:
        if not isinstance(value, RandomState):
            msg = "Expected numpy RandomState, got {}".format(type(value))
            raise PydanticCustomError('validation_error', msg)
        return value
    
    @classmethod
    def __pydantic_get_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)