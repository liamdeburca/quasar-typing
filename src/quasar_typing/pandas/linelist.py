from pandas import DataFrame
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

REQUIRED_COLUMNS = [
    'name', 'n_max', 'needs_line',
    'line',
    'strength_lower', 'strength_upper',
    'v_off_lower', 'v_off_upper',
    'sigma_v_lower', 'sigma_v_upper',
    'is_copy_of',
    'scale_init', 'scale_lower', 'scale_upper'
]

def _validate(value: object) -> object:
    if not isinstance(value, DataFrame):
        msg = "Expected pandas DataFrame, got {}".format(
            type(value).__name__,
        )
        raise PydanticCustomError('validation_error', msg)
    
    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in value.columns
    ]
    if len(missing_columns) > 0:
        msg = "Line list DataFrame is missing required columns: "\
            "{}".format(", ".join(missing_columns))
        raise PydanticCustomError('validation_error', msg)

    return value

class LineList_(DataFrame):
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
        return no_info_plain_validator_function(_validate)