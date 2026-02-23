from astropy.table import QTable
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class QTable_(QTable):
    """
    Type hint for validating any QTable with pydantic.
    """
    @classmethod
    def _validate(value: object) -> object:
        if not isinstance(value, QTable):
            msg = "Expected astropy QTable, got {}".format(
                type(value).__name__,
            )
            raise PydanticCustomError('validation_error', msg)

        return value
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)