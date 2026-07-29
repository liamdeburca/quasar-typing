__all__ = ["rv_continuous_frozen_", "rv_histogram_"]

from typing import Self

from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function
from scipy.stats import rv_histogram
from scipy.stats._distn_infrastructure import rv_continuous_frozen


class rv_continuous_frozen_(rv_continuous_frozen):
    """
    scipy.stats.rv_continuous_frozen
    """

    @classmethod
    def _validate(cls, value: object) -> Self:
        if not isinstance(value, rv_continuous_frozen):
            msg = f"Expected a rv_continuous_frozen, got {type(value).__name__}"
            raise PydanticCustomError("rv_continuous_frozen_type_error", msg)
        return value

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)


class rv_histogram_(rv_histogram):
    """
    scipy.stats.rv_histogram
    """

    @classmethod
    def _validate(cls, value: object) -> Self:
        if not isinstance(value, rv_histogram):
            msg = f"Expected a rv_histogram, got {type(value).__name__}"
            raise PydanticCustomError("rv_histogram_type_error", msg)
        return value

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)
