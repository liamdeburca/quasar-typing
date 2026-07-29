__all__ = ["DynamicNestedSampler_"]

from typing import Self

from dynesty import DynamicNestedSampler
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function


class DynamicNestedSampler_(DynamicNestedSampler):
    """
    dynesty.DynamicNestedSampler
    """

    @classmethod
    def _validate(cls, value: object) -> Self:
        if not isinstance(value, DynamicNestedSampler):
            msg = f"Expected a DynamicNestedSampler, got {type(value).__name__}"
            raise PydanticCustomError("validation_error", msg)
        return value

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)
