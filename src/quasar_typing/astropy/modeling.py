from typing import Any, TypeVar, cast, get_args

from astropy import modeling
from pydantic import (
    GetCoreSchemaHandler,
    PydanticSchemaGenerationError,
    TypeAdapter,
)
from pydantic_core import (
    CoreSchema,
    PydanticCustomError,
)
from pydantic_core.core_schema import no_info_plain_validator_function

from ..utils import isinstance_func


class ModelType(modeling.Model):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(modeling.Model)
        )


class Fittable1DModelType(modeling.Fittable1DModel):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(modeling.Fittable1DModel)
        )


class ParameterType(modeling.Parameter):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(modeling.Parameter)
        )
    
T = TypeVar("T", bound=Fittable1DModelType)


class CompoundModelType[T](modeling.CompoundModel):
    """Typed CompoundModel with submodel type validation via get_args()."""

    def __getitem__(self, index: Any) -> T:
        return cast(T, super().__getitem__(index))

    def __iter__(self) -> T:
        return cast(T, super().__iter__())

    @classmethod
    def validate(
        cls, 
        value: Any, 
        source_type: Any = None,
    ) -> modeling.CompoundModel:
        """Validate a CompoundModel, optionally checking submodel types.

        Parameters
        ----------
        value : Any
            The value to validate.
        source_type : Any, optional
            The parameterized source type (e.g., CompoundModelType[Gaussian1D]).
            If provided and has type args, validates that submodels match.

        Returns
        -------
        CompoundModel
            The validated CompoundModel.

        Raises
        ------
        PydanticCustomError
            If validation fails.
        """
        value = isinstance_func(modeling.CompoundModel)(value)
        args = get_args(source_type) if source_type is not None else ()
        subtype: type = args[0] if args else Any
        [
            TypeAdapter(subtype).validate_python(submodel)
            for submodel in value
        ]
        return value

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        return no_info_plain_validator_function(
            lambda v: cls.validate(v, source_type=source_type)
        )


    @classmethod
    def __class_getitem__(cls, item: Any) -> Any:
        try:
            TypeAdapter(item)
        except PydanticSchemaGenerationError:
            raise TypeError(f"Cannot generate validation schema for {item}")
        return super().__class_getitem__(item)
