from typing import Annotated

import pandas
from pydantic import BeforeValidator
from pydantic_core.core_schema import no_info_plain_validator_function

from .utils import isinstance_func


class StrictDataFrameType(pandas.DataFrame):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(pandas.DataFrame)
        )

type DataFrameType = Annotated[
    StrictDataFrameType, 
    BeforeValidator(pandas.DataFrame),
]