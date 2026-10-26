__all__ = [
    "CosmologyName",
    "StrictCosmologyName"
]

from typing import Annotated

from pydantic_core import PydanticCustomError

from quasar_typing.utils import (
    after_validator_decorator,
    before_validator_decorator,
)

AVAILABLE: tuple[str] = (
    "WMAP1",
    "WMAP3",
    "WMAP5",
    "WMAP7",
    "WMAP9",
    "Planck13",
    "Planck15",
    "Planck18"
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
