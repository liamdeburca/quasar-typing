from astropy.table import Column
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class Column_(Column):
    """
    Type hint for validating any Column with pydantic.
    """
    @classmethod
    def _validate(value: object) -> object:
        if not isinstance(value, Column):
            msg = "Expected astropy Column, got {}".format(
                type(value).__name__,
            )
            raise PydanticCustomError('validation_error', msg)

        return value
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)