from typing import Literal

FWHMStrategy  = Literal['narrowest', 'average', 'widest']
Scale         = Literal['global', 'semilocal', 'local']
Variant       = Literal['spectrum', 'standard', 'flexible', 'rigid']
BootstrapType = Literal['spectrum', 'model', 'frequentist']

VaryLines   = frozenset[Literal['all'] | float]
OutWaves    = frozenset[Literal['all'] | float]
OutMeasures = frozenset[Literal['all'] | str]

# pl: power law, fe: iron emission, ba: Balmer (pseudo)continuum, 
# hg: host galaxy, em: emission lines
FluxComponent = Literal['pl', 'fe', 'ba', 'hg', 'em']
BGFlux = frozenset[FluxComponent]

# raw: linear regression, sc: sigma-clipped linear regression
Suffix = Literal['raw', 'sc']