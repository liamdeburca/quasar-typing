__all__ = ["CacheType", "LRUCacheType"]

try:
    from cachetools import Cache, LRUCache
except ImportError as e:
    raise ImportError(
        "cachetools is required to use quasar_typing.cachetools. "
        "Install it with: pip install cachetools"
    ) from e

from .utils import isinstance_func


class CacheType(Cache):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core.core_schema import no_info_plain_validator_function
        return no_info_plain_validator_function(
            isinstance_func(Cache)
        )


class LRUCacheType(LRUCache):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core.core_schema import no_info_plain_validator_function
        return no_info_plain_validator_function(
            isinstance_func(LRUCache)
        )