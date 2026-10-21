from importlib import import_module

import_module("h5py")

from h5py import AttributeManager, Dataset, File, Group
from pydantic_core.core_schema import no_info_plain_validator_function

from quasar_typing.utils import isinstance_func


class AttributeManagerType(AttributeManager):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(AttributeManager)
        )


class DatasetType(Dataset):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(Dataset)
        )


class GroupType(Group):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(Group)
        )


class FileType(File):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(File)
        )