__all__ = [
    "BootstrapType",
    "FWHMStrategy",
    "FluxComponent",
    "FluxContributions",
    "LawName",
    "MCMCSamplingMethod",
    "MapName",
    "Method",
    "Scale",
    "Suffix",
    "Variant",
]
from typing import Annotated, Literal

from quasar_typing.utils import before_validator_decorator

coerce_to_simple_string = before_validator_decorator(
    lambda s: str(s).strip().lower()
)
ensure_leading_dot = before_validator_decorator(
    lambda s: s if s.startswith(".") else f".{s}"
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
type MapName = Annotated[
    Literal["sfd", "csfd"], 
    coerce_to_simple_string,
]
type LawName = Annotated[
    Literal["ccm89", "o94"],
    coerce_to_simple_string,
]
type JSONExt = Annotated[
    Literal[".json", ".yaml", ".yml", ".toml", ".toon"],
    coerce_to_simple_string,
    ensure_leading_dot,
]
