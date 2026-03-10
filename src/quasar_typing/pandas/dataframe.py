from pandas import DataFrame
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class DataFrame_(DataFrame):
    """
    pandas.DataFrame
    """
    @classmethod
    def _validate(cls, value: object) -> DataFrame:
        if not isinstance(value, DataFrame):
            msg = f"Expected pandas DataFrame, got {type(value).__name__}"
            raise PydanticCustomError('validation_error', msg)
        return value

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)