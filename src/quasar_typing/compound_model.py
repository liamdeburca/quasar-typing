"""
This module defines TypedCompoundModel for validating Astropy CompoundModels 
with Pydantic.
"""
from typing import Any, Tuple, Type, Union

from astropy.modeling import CompoundModel, Model
from pydantic import GetCoreSchemaHandler

class TypedCompoundModel:
    """
    A class designed to bridge the gap between Astropy's CompoundModel and
    Pydantic type validation.
    """

    def __class_getitem__(
        cls, expected_types: Union[Type[Model], Tuple[Type[Model], ...]]
    ) -> Type[CompoundModel]:
        from astropy.modeling import CompoundModel
        from pydantic_core import CoreSchema
        from pydantic_core.core_schema import ValidationInfo

        # Ensure items is a tuple of types
        if not isinstance(expected_types, tuple):
            expected_types = (expected_types,)

        class _TypedCompoundModel(CompoundModel):
            # Store configuration on the generated class
            _expected_types: Tuple[Type[Model], ...] = expected_types

            @classmethod
            def __get_pydantic_core_schema__(
                cls, source_type: Any, handler: GetCoreSchemaHandler,
            ) -> CoreSchema:
                from pydantic_core.core_schema import (
                    with_info_plain_validator_function,
                    plain_serializer_function_ser_schema
                )
                # Return a schema that uses the custom validate method
                return with_info_plain_validator_function(
                    cls.validate,
                    serialization=plain_serializer_function_ser_schema(
                        lambda x: x  # Pass-through serializer for Astropy objects
                    ),
                )

            @classmethod
            def validate(cls, value: Any, info: ValidationInfo) -> Model:
                from astropy.modeling import CompoundModel
                from pydantic_core import ValidationError

                if not isinstance(value, CompoundModel):
                    msg = "Expected CompoundModel, got {}".format(
                        type(value).__name__,
                    )
                    raise ValidationError(msg, info)
                
                value: CompoundModel = value
                for submodel in value:
                    if not isinstance(submodel, cls._expected_types):
                        msg = "Expected CompoundModel to consist only of " \
                            "{} instances, got {}.".format(
                                ', '.join(t.__name__ for t in cls._expected_types),
                                type(submodel).__name__,
                        )
                        raise ValidationError(msg, info)
                    
                return value

        # Set standard class attributes for debugging and introspection
        type_names = ", ".join(t.__name__ for t in expected_types)
        _TypedCompoundModel.__name__ = f"TypedCompoundModel[{type_names}]"
        _TypedCompoundModel.__qualname__ = f"TypedCompoundModel[{type_names}]"
        
        return _TypedCompoundModel
