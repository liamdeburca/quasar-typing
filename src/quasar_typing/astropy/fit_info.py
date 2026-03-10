from scipy.optimize import OptimizeResult
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class OptimizeResult_(OptimizeResult):
    """
    scipy.optimize.OptimizeResult
    """
    @classmethod
    def _validate(cls, value: object) -> OptimizeResult:
        if not isinstance(value, OptimizeResult):
            msg = f"Expected scipy OptimizeResult, got {type(value).__name__}"
            raise PydanticCustomError('validation_error', msg)
        return value
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)
    
class FitInfo(OptimizeResult_):
    """
    scipy.optimize.OptimizeResult
    """
    pass