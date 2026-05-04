__all__ = [
    'Pool_',
    'StringSelection',
    'Method', 'FWHMStrategy', 'Scale', 'Variant', 'BootstrapType',
    'FluxComponent', 'FluxContributions', 'Suffix',
    'BackgroundFlux', 'ModelTypes', 'DataTypes',
    'OutLines', 'OutMeasures',
]
from typing import Literal
from .pool import Pool_
from .string_selection import StringSelection

from .literals import (
    Method, FWHMStrategy, Scale, Variant, BootstrapType, FluxComponent, 
    FluxContributions, Suffix,
)

BackgroundFlux = StringSelection[Literal['pl', 'fe', 'ba', 'hg', 'em']]
ModelTypes = StringSelection[Literal['pl', 'fe', 'ba', 'hg', 'em']]
DataTypes = StringSelection[Literal['pl', 'fe', 'ba', 'hg', 'em']]

VaryLines = StringSelection[str]
OutLines = StringSelection[str]
OutMeasures = StringSelection[str]