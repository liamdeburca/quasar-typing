from typing import Annotated

try:
    from pandas.core.frame import DataFrame
except ImportError as e:
    raise ImportError(
        "pandas is required to use quasar_typing.pandas. "
        "Install it with: pip install pandas"
    ) from e

from pydantic import BeforeValidator

from .utils import isinstance_func


class StrictDataFrameType(DataFrame):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core.core_schema import no_info_plain_validator_function
        return no_info_plain_validator_function(
            isinstance_func(DataFrame)
        )

type DataFrameType = Annotated[
    StrictDataFrameType, 
    BeforeValidator(DataFrame),
]