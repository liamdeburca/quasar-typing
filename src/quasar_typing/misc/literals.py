__all__ = [
    'Method',
    'FWHMStrategy',
    'Scale',
    'Variant',
    'BootstrapType',
    'FluxComponent',
    'FluxContributions',
    'Suffix',
]
from typing import Literal, FrozenSet

type Method = Literal['bootstrap']
type FWHMStrategy = Literal['narrowest', 'average', 'widest']
type Scale = Literal['global', 'semilocal', 'local']
type Variant = Literal['spectrum', 'standard', 'flexible', 'rigid']
type BootstrapType = Literal['spectrum', 'model', 'frequentist']
type FluxComponent = Literal['pl', 'fe', 'ba', 'hg', 'em']
type FluxContributions = FrozenSet[FluxComponent]
type Suffix = Literal['raw', 'sc']