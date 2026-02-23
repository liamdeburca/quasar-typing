from typing import Literal

FWHMStrategy_  = Literal['narrowest', 'average', 'widest']
Scale_         = Literal['global', 'semilocal', 'local']
Variant_       = Literal['spectrum', 'standard', 'flexible', 'rigid']
BootstrapType_ = Literal['spectrum', 'model', 'frequentist']

VaryLines_   = frozenset[Literal['all'] | float]
OutWaves_    = frozenset[Literal['all'] | float]
OutMeasures_ = frozenset[Literal['all'] | str]

# pl: power law, fe: iron emission, ba: Balmer (pseudo)continuum, 
# hg: host galaxy, em: emission lines
FluxComponent_ = Literal['pl', 'fe', 'ba', 'hg', 'em']
BGFlux_ = frozenset[FluxComponent_]

# raw: linear regression, sc: sigma-clipped linear regression
Suffix_ = Literal['raw', 'sc']