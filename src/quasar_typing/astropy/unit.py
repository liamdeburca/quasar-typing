from astropy.units import Unit
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class Unit_(Unit):
    """
    astropy.units.Unit
    """
    @classmethod
    def _validate(cls, value: object) -> Unit:
        if isinstance(value, str):
            try:
                value = Unit(value)
                assert isinstance(value, Unit)
            except ValueError:
                msg = f"Failed to coerce string to astropy Unit"
                raise PydanticCustomError('validation_error', msg)
            except AssertionError:
                msg = f"Coerced value is not an astropy Unit"
                raise PydanticCustomError('validation_error', msg)
        elif not isinstance(value, Unit):
            msg = f"Expected astropy Unit, got {type(value).__name__}"
            raise PydanticCustomError('validation_error', msg)
        return value
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)