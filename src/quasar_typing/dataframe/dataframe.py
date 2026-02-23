from pandas import DataFrame

class DataFrameLike(DataFrame):
    """
    Type hint for validating any DataFrame with pydantic.
    """
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema

        def validate(value: object) -> object:
            from pydantic_core import PydanticCustomError
            from pandas import DataFrame

            if not isinstance(value, DataFrame):
                msg = "Expected pandas DataFrame, got {}".format(
                    type(value).__name__,
                )
                raise PydanticCustomError('validation_error', msg)

            return value            
        
        return core_schema.no_info_plain_validator_function(validate)