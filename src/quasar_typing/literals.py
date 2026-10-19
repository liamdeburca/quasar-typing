__all__ = [
    "BootstrapType",
    "FWHMStrategy",
    "FluxComponent",
    "FluxContributions",
    "MCMCSamplingMethod",
    "Method",
    "Scale",
    "Suffix",
    "Variant",
]
from typing import Annotated, Literal

from .utils import before_validator_decorator

coerce_to_simple_string = before_validator_decorator(
    lambda s: str(s).strip().lower()
)

type Method = Annotated[
    Literal["bootstrap"],
    coerce_to_simple_string,
]
type FWHMStrategy = Annotated[
    Literal["narrowest", "average", "widest"],
    coerce_to_simple_string,
]
type Scale = Annotated[
    Literal["global", "semilocal", "local"],
    coerce_to_simple_string,
]
type Variant = Annotated[
    Literal["spectrum", "standard", "flexible", "rigid"],
    coerce_to_simple_string,
]
type BootstrapType = Annotated[
    Literal["spectrum", "model", "frequentist"],
    coerce_to_simple_string,
]
type FluxComponent = Annotated[
    Literal["pl", "fe", "ba", "hg", "em"],
    coerce_to_simple_string,
]
type FluxContributions = frozenset[FluxComponent]
type Suffix = Annotated[
    Literal["raw", "sc"],
    coerce_to_simple_string,
]
type MCMCSamplingMethod = Annotated[
    Literal["fisher", "uniform"],
    coerce_to_simple_string,
]