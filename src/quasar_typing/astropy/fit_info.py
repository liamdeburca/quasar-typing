from scipy.optimize import OptimizeResult
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class FitInfo_(OptimizeResult):
    """
    Type hint for validating astropy FitInfo with pydantic.
    """
    @classmethod
    def _validate(cls, value: object) -> OptimizeResult:
        if not isinstance(value, OptimizeResult):
            msg = "Expected scipy OptimizeResult, got {}".format(
                type(value).__name__,
            )
            raise PydanticCustomError('validation_error', msg)

        return value
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)
