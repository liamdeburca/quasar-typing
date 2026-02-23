from typing import Union

from .path import *
from .file import *
from .dir import *

from .fits import *

AnyFileLike = Union[AbsoluteFileLike, RelativeFileLike]