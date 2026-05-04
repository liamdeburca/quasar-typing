__all__ = ['LineList']

from pandas import DataFrame
from pydantic_core import PydanticCustomError
from .dataframe import DataFrame_

class LineList(DataFrame_):
    """
    pandas.DataFrame with specific columns (see LineList.REQUIRED_COLUMNS)
    """
    REQUIRED_COLUMNS = [
        'name', 
        'n_max', 
        'needs_line',
        'line',
        'strength_lower', 
        'strength_upper',
        'v_off_lower', 
        'v_off_upper',
        'sigma_v_lower', 
        'sigma_v_upper',
        'is_copy_of',
        'scale_init', 
        'scale_lower', 
        'scale_upper'
    ]

    @classmethod
    def _validate(cls, value: object) -> DataFrame:
        if not isinstance(value, DataFrame):
            value = super()._validate(value)
        
        missing_columns = [
            col for col in cls.REQUIRED_COLUMNS
            if col not in value.columns
        ]
        if len(missing_columns) > 0:
            cols = ", ".join(missing_columns)
            msg = f"Line list DataFrame is missing required columns: {cols}"
            raise PydanticCustomError('validation_error', msg)

        return value