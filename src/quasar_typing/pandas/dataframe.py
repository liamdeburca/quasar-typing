from pandas import DataFrame
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

def _validate(value: object) -> object:
    if not isinstance(value, DataFrame):
        msg = "Expected pandas DataFrame, got {}".format(
            type(value).__name__,
        )
        raise PydanticCustomError('validation_error', msg)

    return value

class DataFrame_(DataFrame):
    """
    Type hint for validating any DataFrame with pydantic.
    """
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(_validate)