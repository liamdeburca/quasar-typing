from astropy.modeling.core import Fittable1DModel
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class Fittable1DModel_(Fittable1DModel):
    """
    Type hint for validating astropy Fittable1DModel with pydantic.
    """
    @classmethod
    def _validate(value: object) -> object:
        if not isinstance(value, Fittable1DModel):
            msg = "Expected astropy Fittable1DModel, got {}".format(
                type(value).__name__,
            )
            raise PydanticCustomError('validation_error', msg)

        return value
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)