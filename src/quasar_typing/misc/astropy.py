from typing import Callable, Union
from scipy.optimize import OptimizeResult
from astropy.units.quantity import Quantity
from astropy.modeling.core import Fittable1DModel, CompoundModel
from astropy.table import QTable, Column

from .any import AnyTypeGenerator
from ..arrays import FloatVector

Fittable1DModelLike = AnyTypeGenerator[Fittable1DModel]
CompoundModelLike   = AnyTypeGenerator[CompoundModel]
ModelLike           = Union[Fittable1DModelLike, CompoundModelLike]

FitInfoLike = AnyTypeGenerator[OptimizeResult]

FitterLike = Callable[
    [ModelLike, FloatVector, FloatVector, FloatVector, bool],
    tuple[ModelLike, OptimizeResult],
]
QuantityLike = AnyTypeGenerator[Quantity]
QTableLike = AnyTypeGenerator[QTable]
ColumnLike = AnyTypeGenerator[Column]