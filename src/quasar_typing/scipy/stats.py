__all__ = [
    "RVContinuous",
    "RVContinuousFrozen",
    "RVHistogram",
]

from scipy.stats import rv_continuous, rv_histogram

# Try to import from public API first, fall back to private API
try:
    from scipy.stats import rv_continuous_frozen
except ImportError:
    # Fallback to private API for older scipy versions
    from scipy.stats._distn_infrastructure import rv_continuous_frozen

from ..utils import isinstance_func

### scipy.stats

class RVHistogram(rv_histogram):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import PydanticCustomError
        from pydantic_core.core_schema import no_info_plain_validator_function
        def _validate(value: object):
            if isinstance(value, rv_histogram):
                return value

            try:
                value = rv_histogram(value)
            except Exception as exc:
                raise PydanticCustomError(
                    "validation_error",
                    f"Failed to coerce value of type {type(value).__name__} "
                    f"to scipy.stats.rv_histogram"
                ) from exc
            return value
        return no_info_plain_validator_function(_validate)

class RVContinuous(rv_continuous):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core.core_schema import no_info_plain_validator_function
        return no_info_plain_validator_function(
            isinstance_func(rv_continuous)
        )

class RVContinuousFrozen(rv_continuous_frozen):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core.core_schema import no_info_plain_validator_function
        return no_info_plain_validator_function(
            isinstance_func(rv_continuous_frozen)
        )