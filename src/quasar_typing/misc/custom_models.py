from typing import Union
from astropy.modeling.core import CompoundModel
from .any import AnyTypeGenerator, AnyModelGenerator

GaussianModelLike      = AnyModelGenerator['GaussianModel']
PowerLawModelLike      = AnyModelGenerator['PowerLawModel']
PLWiggleLike           = AnyModelGenerator['PLWiggle']
TemplateModelLike      = AnyModelGenerator['TemplateModel']
SplitTemplateModelLike = AnyModelGenerator['SplitTemplateModelLike']

LinesLike    = Union[GaussianModelLike, AnyTypeGenerator[CompoundModel]]
PowerLawLike = Union[PowerLawModelLike, PLWiggleLike]
TemplateLike = Union[TemplateModelLike, AnyTypeGenerator[CompoundModel]]