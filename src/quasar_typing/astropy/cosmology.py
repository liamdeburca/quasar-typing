__all__ = [
    "CosmologyName",
    "CosmologyType",
    "StrictCosmologyName"
]

from typing import Annotated

from astropy.cosmology import Cosmology
from astropy.cosmology.realizations import available as AVAILABLE
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

from quasar_typing.utils import (
    after_validator_decorator,
    before_validator_decorator,
    isinstance_func,
)


@before_validator_decorator
def coerce_to_cosmology_name(value: str) -> str:
    if not isinstance(value, str):
        # Let pydantic handle the type error by returning as-is
        return value
    value = value.strip().lower()
    for candidate in AVAILABLE:
        if value == candidate.lower():
            return candidate
    return value
    

@after_validator_decorator
def validate_cosmology_name(value: str) -> str:
    if value not in AVAILABLE:
        raise PydanticCustomError(
            "validation_error",
            "Invalid cosmology name. Choose from: {options}",
            {"options": AVAILABLE}
        )
    return value


type StrictCosmologyName = Annotated[str, validate_cosmology_name]
type CosmologyName = Annotated[StrictCosmologyName, coerce_to_cosmology_name]


class CosmologyType(Cosmology):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(Cosmology)
        )
