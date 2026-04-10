from scipy.stats._distn_infrastructure import rv_continuous_frozen
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class rv_continuous_frozen_(rv_continuous_frozen):
    """
    scipy.stats.rv_continuous_frozen
    """
    @classmethod
    def _validate(cls, value: object) -> rv_continuous_frozen:
        if not isinstance(value, rv_continuous_frozen):
            msg = f'Expected a rv_continuous_frozen, got {type(value).__name__}'
            raise PydanticCustomError('rv_continuous_frozen_type_error', msg)
        return value
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)
