from astropy.coordinates import SkyCoord
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class SkyCoord_(SkyCoord):
    """
    astropy.coordinates.SkyCoord
    """
    @classmethod
    def _validate(cls, value: object) -> SkyCoord:
        if isinstance(value, tuple): 
            try: 
                value = SkyCoord(*value)
            except Exception as e:
                msg = f"Failed to coerce tuple {value} to astropy SkyCoord: {e}"
                raise PydanticCustomError('validation_error', msg)
        elif isinstance(value, dict):
            try:
                value = SkyCoord(**value)
            except Exception as e:
                msg = f"Failed to coerce dict {value} to astropy SkyCoord: {e}"
                raise PydanticCustomError('validation_error', msg)            
        elif not isinstance(value, SkyCoord):
            msg = f"Expected astropy SkyCoord, got {type(value).__name__}"
            raise PydanticCustomError('validation_error', msg)
        return value
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)