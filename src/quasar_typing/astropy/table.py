__all__ = [
    "ColumnType",
    "QTableType",
    "RowType",
    "TableType",
]

from astropy.table.column import Column
from astropy.table.row import Row
from astropy.table.table import QTable, Table
from pydantic_core.core_schema import no_info_plain_validator_function

from quasar_typing.utils import isinstance_func


class TableType(Table):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(Table)
        )


class QTableType(QTable):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(QTable)
        )


class RowType(Row):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(Row)
        )


class ColumnType(Column):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(Column)
        )