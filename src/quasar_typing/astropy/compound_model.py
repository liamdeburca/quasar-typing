from typing import TypeVar, Any
from astropy.modeling import CompoundModel
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

from .utils.model_meta import _ModelMeta_

T = TypeVar('T')

class CompoundModel_[T](CompoundModel, metaclass=_ModelMeta_):
    """
    astropy.modeling.CompoundModel with support for type parameter.
    
    Use `CompoundModel_[ModelType]` to specify the types of submodels
    for Pylance type checking.
    """
    _model_type: type | tuple[type, ...] | None = None
    
    @classmethod
    def _validate(cls, value: object) -> CompoundModel:
        if not isinstance(value, CompoundModel):
            msg = f"Expected astropy CompoundModel, got {type(value).__name__}"
            raise PydanticCustomError('validation_error', msg)
        
        # Validate submodel types if specified
        if hasattr(cls, '_model_type') and cls._model_type is not None:
            for i, submodel in enumerate(value):
                if not isinstance(submodel, cls._model_type):
                    msg = f"Type of submodel {i} is not in {cls._model_type}, \
                        has type {type(submodel).__name__}"
                    raise PydanticCustomError('validation_error', msg)
        
        return value
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)
        
    def __class_getitem__(cls, subtypes: type | tuple[type, ...]) -> type['CompoundModel_[T]']:
        """Create a typed CompoundModel_ for type checking and validation."""
        # if not isinstance(subtypes, tuple):
        #     subtypes = (subtypes,)

        class TypedCompoundModel_(CompoundModel_):
            _model_type = subtypes
                    
        return TypedCompoundModel_
    
    def __getitem__(self, index: Any) -> T:
        return super().__getitem__(index)
    
    def __iter__(self) -> T:
        return super().__iter__()