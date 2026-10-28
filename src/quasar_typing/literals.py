__all__ = [
    "BalmerSeriesTemplateName",
    "BootstrapType",
    "FWHMStrategy",
    "FluxComponent",
    "FluxContributions",
    "HostGalaxyTemplateName",
    "LawName",
    "LineType",
    "MCMCSamplingMethod",
    "MapName",
    "Method",
    "ModelName",
    "ParameterName",
    "Scale",
    "Suffix",
    "TemplateName",
    "Variant",
]
from typing import Annotated, Literal

from pydantic import StringConstraints

from quasar_typing.utils import before_validator_decorator

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
    StringConstraints(pattern="^..+"),
]

### quasar-models

type ModelName = Annotated[str, StringConstraints(min_length=1)]
type ParameterName = ModelName

type TemplateName = Annotated[
    str,
    coerce_to_simple_string,
    StringConstraints(min_length=1),
]
type BalmerSeriesTemplateName = Annotated[
    Literal["sh1995"],
    coerce_to_simple_string,
]
type HostGalaxyTemplateName = Annotated[
    Literal["bc2003"],
    coerce_to_simple_string,
]
type LineType = Annotated[
    Literal["n", "b"],
    coerce_to_simple_string,
]