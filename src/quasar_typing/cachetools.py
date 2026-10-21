__all__ = ["CacheType", "LRUCacheType"]

from importlib import import_module

import_module("cachetools")

from cachetools import Cache, LRUCache
from pydantic_core.core_schema import no_info_plain_validator_function

from quasar_typing.utils import isinstance_func


class CacheType(Cache):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(Cache)
        )


class LRUCacheType(LRUCache):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(LRUCache)
        )