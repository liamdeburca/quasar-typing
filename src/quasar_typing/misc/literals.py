from typing import Literal, Union

FWHMStrategyLike = Literal['narrowest', 'average', 'widest']
ScaleLike =  Literal['global', 'semilocal', 'local']
VariantLike = Literal['spectrum', 'standard', 'flexible', 'rigid']
BootstrapTypeLike = Literal['spectrum', 'model', 'frequentist']
VaryLinesLike = set[Union[Literal['all'], float]]
OutWavesLike = set[Union[Literal['all'], float]]
OutMeasuresLike = set[Union[Literal['all'], str]]

BGFluxLike = set[Literal['pl', 'fe', 'em']]
_BGFluxLike = frozenset[Literal['pl', 'fe', 'em']]
SuffixLike = Literal['raw', 'sc']