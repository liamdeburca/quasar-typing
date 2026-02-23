__all__ = [
    'RandomStateLike'
]

from numpy import array
from numpy.random import RandomState, BitGenerator
from pydantic_core import PydanticCustomError

class RandomStateLike(RandomState):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value, _info) -> RandomState:
        if isinstance(value, RandomState):
            pass
        elif (value is None) or isinstance(value, (int, BitGenerator)):
            value = RandomState(value)
        else:
            try:
                value = array(value)
            except:
                msg = "Value must be 'None', or of type 'int', 'BitGenerator',"\
                    "'array_like', or 'RandomState', but is '{}'!" \
                    .format(type(value).__name__)
                raise PydanticCustomError('validation_error', msg)

        return value