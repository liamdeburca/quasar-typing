from astropy.modeling import Model
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

from .utils.model_meta import _ModelMeta_


class Model_(Model, metaclass=_ModelMeta_):
    """
    astropy.modeling.Model
    """

    @classmethod
    def _validate(cls, value: object) -> Model:
        if not isinstance(value, Model):
            msg = f"Expected astropy Model, got {type(value).__name__}"
            raise PydanticCustomError("validation_error", msg)
        return value

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)
