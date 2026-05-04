__all__ = ['_ModelMeta_']

from typing import Union
from astropy.modeling.core import _ModelMeta

class _ModelMeta_(_ModelMeta):
    def __or__(cls, other): 
        return Union[cls, other]    
    
    def __ror__(cls, other): 
        return Union[other, cls]