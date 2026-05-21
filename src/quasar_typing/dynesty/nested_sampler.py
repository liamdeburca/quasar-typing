__all__ = ['NestedSampler_']

from typing import Self
from dynesty import NestedSampler
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class NestedSampler_(NestedSampler):
    """
    dynesty.NestedSampler
    """
    @classmethod
    def _validate(cls, value: object) -> Self:
        if not isinstance(value, NestedSampler):
            msg = f'Expected a NestedSampler, got {type(value).__name__}'
            raise PydanticCustomError('validation_error', msg)
        return value
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)