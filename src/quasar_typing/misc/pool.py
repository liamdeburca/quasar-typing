from multiprocessing.pool import Pool
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class Pool_(Pool):
    """
    multiprocessing.pool.Pool
    """
    @classmethod
    def _validate(cls, value: object) -> Pool:
        if not isinstance(value, Pool):
            msg = f"Expected multiprocessing.pool.Pool, got {type(value).__name__}"
            raise PydanticCustomError('validation_error', msg)
        return value
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)