from typing import Callable
from astropy.modeling.fitting import (
    Fitter, LevMarLSQFitter, DogBoxLSQFitter, TRFLSQFitter,
)
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

from ..numpy import FittableFloatVector
from .fit_info import FitInfo
from .model import Model_

AVAILABLE_FITTERS: list = [
    LevMarLSQFitter,
    DogBoxLSQFitter,
    TRFLSQFitter,
]

FitterInstance = Callable[
    [
        Model_, 
        FittableFloatVector, 
        FittableFloatVector, 
        FittableFloatVector, 
        bool,
    ],
    tuple[
        Model_, 
        FitInfo,
    ]
]
FitterInstance.__doc__ = \
    "convenience function wrapping the Fitter.__call__ method"

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