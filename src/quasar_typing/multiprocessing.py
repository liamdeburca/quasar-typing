from multiprocessing.pool import Pool

from pydantic_core.core_schema import no_info_plain_validator_function

from .utils import isinstance_func


class PoolType(Pool):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(Pool)
        )