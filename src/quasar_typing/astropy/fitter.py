from astropy.modeling.fitting import (
    Fitter, LevMarLSQFitter, DogBoxLSQFitter, TRFLSQFitter,
)
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

AVAILABLE_FITTERS: list = [
    LevMarLSQFitter,
    DogBoxLSQFitter,
    TRFLSQFitter,
]

class Fitter_(Fitter):
    """
    Type hint for validating astropy Fitter with pydantic.
    """
    @classmethod
    def _validate(value: object) -> object:
        if not isinstance(value, Fitter):
            msg = "Expected astropy Fitter, got {}".format(
                type(value).__name__,
            )
            raise PydanticCustomError('validation_error', msg)
        
        if not any(isinstance(value, fitter) for fitter in AVAILABLE_FITTERS):
            msg = "Expected astropy Fitter of type {}, got {}".format(
                ", ".join(fitter.__name__ for fitter in AVAILABLE_FITTERS),
                type(value).__name__,
            )
            raise PydanticCustomError('validation_error', msg)

        return value
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)