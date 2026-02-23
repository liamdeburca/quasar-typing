from logging import Logger
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class Logger_(Logger):
    @classmethod
    def _validate(cls, value: object) -> Logger:
        if not isinstance(value, Logger):
            msg = "Expected logging Logger, got {}".format(
                type(value).__name__,
            )
            raise PydanticCustomError('validation_error', msg)
        return value
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)
