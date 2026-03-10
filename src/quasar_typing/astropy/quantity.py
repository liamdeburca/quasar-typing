from astropy.units import Quantity
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class Quantity_(Quantity):
    """
    astropy.units.Quantity
    """
    @classmethod
    def _validate(cls, value: object) -> Quantity:
        if not isinstance(value, Quantity):
            msg = f"Expected astropy Quantity, got {type(value).__name__}"
            raise PydanticCustomError('validation_error', msg)
        return value
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)