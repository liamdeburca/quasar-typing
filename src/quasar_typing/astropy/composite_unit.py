from astropy.units import CompositeUnit
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class CompositeUnit_(CompositeUnit):
    """
    astropy.units.CompositeUnit
    """
    @classmethod
    def _validate(cls, value: object) -> CompositeUnit:
        if isinstance(value, str):
            try:
                value = CompositeUnit(value)
                assert isinstance(value, CompositeUnit)
            except ValueError:
                msg = "Failed to coerce string to astropy CompositeUnit"
                raise PydanticCustomError('validation_error', msg)
            except AssertionError:
                msg = "Coerced value is not an astropy CompositeUnit"
                raise PydanticCustomError('validation_error', msg)
        elif not isinstance(value, CompositeUnit):
            msg = f"Expected astropy CompositeUnit, got {type(value).__name__}"
            raise PydanticCustomError('validation_error', msg)
        return value
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)