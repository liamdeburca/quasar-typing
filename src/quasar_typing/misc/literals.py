__all__ = [
    "BootstrapType",
    "FWHMStrategy",
    "FluxComponent",
    "FluxContributions",
    "Method",
    "Scale",
    "Suffix",
    "Variant",
]
from typing import Literal

type Method = Literal["bootstrap"]
type FWHMStrategy = Literal["narrowest", "average", "widest"]
type Scale = Literal["global", "semilocal", "local"]
type Variant = Literal["spectrum", "standard", "flexible", "rigid"]
type BootstrapType = Literal["spectrum", "model", "frequentist"]
type FluxComponent = Literal["pl", "fe", "ba", "hg", "em"]
type FluxContributions = frozenset[FluxComponent]
type Suffix = Literal["raw", "sc"]
