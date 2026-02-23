from pandas import DataFrame

class LineListLike(DataFrame):
    """
    Type hint for validating line list DataFrames with pydantic.
    """
    required_columns: list[str] = [
        'name', 'n_max', 'needs_line',
        'line', 
        'strength_lower', 'strength_upper',
        'v_off_lower', 'v_off_upper', 
        'sigma_v_lower', 'sigma_v_upper',
        'is_copy_of',
        'scale_init', 'scale_lower', 'scale_upper'
    ]
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
            
            missing_columns = [
                col for col in cls.required_columns
                if col not in value.columns
            ]
            if len(missing_columns) > 0:
                msg = "Line list DataFrame is missing required columns: "\
                    "{}".format(", ".join(missing_columns))
                raise PydanticCustomError('validation_error', msg)

            return value            
        
        return core_schema.no_info_plain_validator_function(validate)