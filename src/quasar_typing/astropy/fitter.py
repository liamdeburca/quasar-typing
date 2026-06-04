__all__ = [
    'Fitter_',
]

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
    astropy.modeling.fitting.Fitter
    """
    @classmethod
    def _validate(cls, value: object) -> Fitter:
        if not isinstance(value, Fitter):
            msg = f"Expected astropy Fitter, got {type(value).__name__}"
            raise PydanticCustomError('validation_error', msg)
        
        if not any(isinstance(value, fitter) for fitter in AVAILABLE_FITTERS):
            msg = (
                f"Expected astropy Fitter of type "
                f"{', '.join(fitter.__name__ for fitter in AVAILABLE_FITTERS)}, "
                f"got {type(value).__name__}"
            )
            raise PydanticCustomError('validation_error', msg)
        return value
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)