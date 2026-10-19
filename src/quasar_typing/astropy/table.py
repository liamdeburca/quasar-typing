
from astropy import table
from pydantic_core.core_schema import no_info_plain_validator_function

from ..utils import isinstance_func


class TableType(table.Table):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(table.Table)
        )


class QTableType(table.QTable):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(table.QTable)
        )


class RowType(table.Row):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(table.Row)
        )


class ColumnType(table.Column):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(table.Column)
        )