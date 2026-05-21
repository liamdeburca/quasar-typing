__all__ = [
    'Pool_',
    'StringSelection',
    'Method', 'FWHMStrategy', 'Scale', 'Variant', 'BootstrapType',
    'FluxComponent', 'FluxContributions', 'Suffix',
    'BackgroundFlux', 'ModelTypes', 'DataTypes',
    'VaryLines', 'OutLines', 'OutMeasures',
    'PowerLawModelParams', 
    'IronModelParams',
    'BalmerModelParams', 
    'HostGalaxyModelParams',
]
from typing import Literal
from .pool import Pool_
from .string_selection import StringSelection

from .literals import (
    Method, FWHMStrategy, Scale, Variant, BootstrapType, FluxComponent, 
    FluxContributions, Suffix,
)

class BackgroundFlux(StringSelection[Literal['pl', 'fe', 'ba', 'hg', 'em']]):
    """
    Lorem ipsum...
    """
    _string_options = ('pl', 'fe', 'ba', 'hg', 'em')

class ModelTypes(StringSelection[Literal['pl', 'fe', 'ba', 'hg', 'em']]):
    """
    Lorem ipsum...
    """
    _string_options = ('pl', 'fe', 'ba', 'hg', 'em')

class DataTypes(StringSelection[Literal['pl', 'fe', 'ba', 'hg', 'em']]):
    """
    Lorem ipsum...
    """
    _string_options = ('pl', 'fe', 'ba', 'hg', 'em')

class VaryLines(StringSelection[str]):
    """
    Lorem ipsum...
    """

class OutLines(StringSelection[str]):
    """
    Lorem ipsum...
    """
    _string_options = ('pl', 'fe', 'ba', 'hg', 'em')

class OutMeasures(StringSelection[str]):
    """
    Lorem ipsum...    
    """

class PowerLawModelParams(StringSelection[Literal['flux', 'alpha']]):
    """
    Lorem ipsum...
    """
    _string_options = ('flux', 'alpha')

class BalmerModelParams(StringSelection[Literal['flux', 'fwhm', 'ratio']]):
    """
    Lorem ipsum...
    """
    _string_options = ('flux', 'fwhm', 'ratio')

class IronModelParams(StringSelection[Literal['flux', 'fwhm', 'split', 'left', 'right']]):
    """
    Lorem ipsum...
    """
    _string_options = ('flux', 'fwhm', 'split', 'left', 'right')

class HostGalaxyModelParams(StringSelection[Literal['flux', 'fwhm']]):
    """
    Lorem ipsum...
    """
    _string_options = ('flux', 'fwhm')