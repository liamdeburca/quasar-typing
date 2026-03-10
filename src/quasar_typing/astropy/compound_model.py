from astropy.modeling import CompoundModel
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class CompoundModel_(CompoundModel):
    """
    astropy.modeling.CompoundModel
    """
    @classmethod
    def _validate(cls, value: object) -> CompoundModel:
        if not isinstance(value, CompoundModel):
            msg = f"Expected astropy CompoundModel, got {type(value).__name__}"
            raise PydanticCustomError('validation_error', msg)
        return value
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)
    
    @classmethod
    def __class_getitem__(cls, subtypes) -> type['CompoundModel_']:
        if not isinstance(subtypes, tuple):
            subtypes = (subtypes,)

        class TypedCompoundModel_(CompoundModel_):
            @classmethod
            def _validate(cls, value: object) -> CompoundModel:
                value: CompoundModel = super()._validate(value)

                for i, submodel in enumerate(value):
                    if not isinstance(submodel, subtypes):
                        msg = f"Type of submodel {i} is not in {subtypes}, \
                            has type {type(submodel).__name__}"
                        raise PydanticCustomError('validation_error', msg)

                return value
                    
        return TypedCompoundModel_