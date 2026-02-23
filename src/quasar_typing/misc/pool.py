from multiprocessing.pool import Pool
from pydantic_core import PydanticCustomError

class PoolLike(Pool):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value, _info) -> Pool:
        if not isinstance(value, Pool):
            msg = "Value mus be of type 'multiprocessing.pool.Pool',"\
                "but is '{}'!"\
                .format(type(value).__name__)
            raise PydanticCustomError('validation_error', msg)            
        
        return value
