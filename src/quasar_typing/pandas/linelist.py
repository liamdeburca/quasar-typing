__all__ = ['LineList']

from pandas import DataFrame
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class LineList(DataFrame):
    """
    pandas.DataFrame with specific columns (see LineList.REQUIRED_COLUMNS)
    """
    REQUIRED_COLUMNS = [
        'name', 'n_max', 'needs_line',
        'line',
        'strength_lower', 'strength_upper',
        'v_off_lower', 'v_off_upper',
        'sigma_v_lower', 'sigma_v_upper',
        'is_copy_of',
        'scale_init', 'scale_lower', 'scale_upper'
    ]

    @classmethod
    def _validate(cls, value: object) -> DataFrame:
        if not isinstance(value, DataFrame):
            msg = f"Expected pandas DataFrame, got {type(value).__name__}"
            raise PydanticCustomError('validation_error', msg)
        
        missing_columns = [
            col for col in cls.REQUIRED_COLUMNS
            if col not in value.columns
        ]
        if len(missing_columns) > 0:
            msg = "Line list DataFrame is missing required columns: "
            msg += ", ".join(missing_columns)
            raise PydanticCustomError('validation_error', msg)

        return value
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)