from typing import Self
from astropy.modeling.core import CompoundModel
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class CompoundModel_(CompoundModel):
    """
    Type hint for validating astropy CompoundModel with pydantic.
    """
    @classmethod
    def _validate(value: object) -> object:
        if not isinstance(value, CompoundModel):
            msg = "Expected astropy CompoundModel, got {}".format(
                type(value).__name__,
            )
            raise PydanticCustomError('validation_error', msg)

        return value
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)
    
    @classmethod
    def __class_getitem__(cls, subtypes) -> Self:
        
        if not isinstance(subtypes, tuple):
            subtypes = (subtypes,)

        class TypedCompoundModel_(CompoundModel_):
            """
            Type hint for validating astropy CompoundModel with pydantic.
            """
            @classmethod
            def _validate(value: object) -> object:
                if not isinstance(value, CompoundModel):
                    msg = "Expected astropy CompoundModel, got {}".format(
                        type(value).__name__,
                    )
                    raise PydanticCustomError('validation_error', msg)

                for subtype in subtypes:
                    if not isinstance(value, subtype):
                        msg = "Expected astropy CompoundModel of type {}, got {}".format(
                            subtype.__name__,
                            type(value).__name__,
                        )
                        raise PydanticCustomError('validation_error', msg)

                return value
        
        return TypedCompoundModel_