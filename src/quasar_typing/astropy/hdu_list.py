from astropy.io.fits import HDUList
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class HDUList_(HDUList):
    """
    astropy.io.fits.HDUList
    """
    @classmethod
    def _validate(cls, value: object) -> HDUList:
        if not isinstance(value, HDUList):
            msg = f"Expected astropy HDUList, got {type(value).__name__}"
            raise PydanticCustomError('validation_error', msg)
        return value
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)