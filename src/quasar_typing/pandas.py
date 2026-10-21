from importlib import import_module

import_module("pandas")

from typing import Annotated

from pandas import DataFrame
from pydantic import BeforeValidator
from pydantic_core.core_schema import no_info_plain_validator_function

from quasar_typing.utils import isinstance_func


class StrictDataFrameType(DataFrame):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(DataFrame)
        )

type DataFrameType = Annotated[StrictDataFrameType, BeforeValidator(DataFrame)]