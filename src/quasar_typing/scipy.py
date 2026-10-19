__all__ = [
    # Sparse
    "BSRArray",
    "BSRMatrix",
    "COOArray",
    "COOMatrix",
    "CSCArray",
    "CSCMatrix",
    "CSRArray",
    "CSRMatrix",
    "DIAArray",
    "DIAMatrix",
    "DOKArray",
    "DOKMatrix",
    "LILArray",
    "LILMatrix",
    # Optimize
    "OptimizeResultType",
    # Stats
    "RVContinuous",
    "RVContinuousFrozen",
    "RVHistogram",
    
    "SparseArray",
    "SparseMatrix",
]
import math
from typing import Annotated, Literal, Self

import numpy as np
from pydantic import validate_call
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function
from scipy import optimize, sparse
from scipy.stats import rv_continuous, rv_histogram
from scipy.stats._distn_infrastructure import rv_continuous_frozen

from quasar_typing.numpy import FloatMatrix, FloatVector

from .utils import isinstance_func, isinstance_validator

### scipy.optimize.OptimizeResult

class OptimizeResultType(optimize.OptimizeResult):
    """
    scipy.optimize.OptimizeResult with Pydantic validation support.
    """
    @validate_call
    def __init__(
        self,
        x: FloatVector,
        cost: float,
        fun: FloatVector,
        jac: FloatMatrix | None,
        grad: FloatVector | None,
        optimality: float | None,
        active_mask: FloatVector | None,
        nfev: int,
        njev: int,
        status: Literal[-1, 0, 1, 2, 3, 4],
        message: str,
        success: bool,
    ):
        self.x: FloatVector = x
        self.cost: float = cost
        self.fun: FloatVector = fun
        self.jac: FloatMatrix | None = jac
        self.grad: FloatVector | None = grad
        self.optimality: float | None = optimality
        self.active_mask: FloatVector | None = active_mask
        self.nfev: int = nfev
        self.njev: int = njev
        self.status: Literal[-1, 0, 1, 2, 3, 4] = status
        self.message: str = message
        self.success: bool = success

    @classmethod
    def fromFitInfo(cls, fit_info: optimize.OptimizeResult) -> Self:
        return cls(
            x=fit_info.x,
            cost=fit_info.cost,
            fun=fit_info.fun,
            jac=fit_info.jac,
            grad=fit_info.grad,
            optimality=fit_info.optimality,
            active_mask=fit_info.active_mask,
            nfev=fit_info.nfev,
            njev=fit_info.njev,
            status=fit_info.status,
            message=fit_info.message,
            success=fit_info.success,
        )

    @classmethod
    def _validate(cls, value: object) -> Self:
        if isinstance(value, cls):
            return value

        if isinstance(value, optimize.OptimizeResult):
            try:
                return cls.fromFitInfo(value)
            except Exception as exc:
                raise PydanticCustomError(
                    "validation_error", 
                    "Could not coerce OptimizeResult to OptimizeResultType",
                ) from exc
        if isinstance(value, dict):
            try:
                return cls(**value)
            except Exception as exc:
                raise PydanticCustomError(
                    "validation_error", 
                    "Could not coerce dictionary to OptimizeResultType",
                ) from exc

        msg = (
            f"Expected an OptimizeResult or {cls.__name__}, "
            f"got {type(value).__name__}"
        )
        raise PydanticCustomError("validation_error", msg)

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)

    @property
    def dof(self) -> int:
        return self.fun.size - self.x.size

    @property
    def chi2(self) -> float:
        return np.dot(self.fun, self.fun)

    @property
    def reduced_chi2(self) -> float:
        dof = self.dof
        return math.inf if dof <= 0 else (self.chi2 / dof)

    @property
    def n_lb(self) -> int:
        return int((self.active_mask == -1).sum())

    @property
    def n_ub(self) -> int:
        return int((self.active_mask == 1).sum())

### scipy.sparse

# Arrays

class SparseArray(sparse.sparray):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(sparse.sparray)
        )

type BSRArray = Annotated[
    SparseArray,
    isinstance_validator(sparse.bsr_array),
]
type COOArray = Annotated[
    SparseArray,
    isinstance_validator(sparse.coo_array),
]
type CSCArray = Annotated[
    SparseArray,
    isinstance_validator(sparse.csc_array),
]
type CSRArray = Annotated[
    SparseArray,
    isinstance_validator(sparse.csr_array),
]
type DIAArray = Annotated[
    SparseArray,
    isinstance_validator(sparse.dia_array),
]
type DOKArray = Annotated[
    SparseArray,
    isinstance_validator(sparse.dok_array),
]
type LILArray = Annotated[
    SparseArray,
    isinstance_validator(sparse.lil_array),
]

# Matrices

class SparseMatrix(sparse.spmatrix):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(sparse.spmatrix)
        )
    
type BSRMatrix = Annotated[
    SparseMatrix,
    isinstance_validator(sparse.bsr_matrix),
]
type COOMatrix = Annotated[
    SparseMatrix,
    isinstance_validator(sparse.coo_matrix),
]
type CSCMatrix = Annotated[
    SparseMatrix,
    isinstance_validator(sparse.csc_matrix),
]
type CSRMatrix = Annotated[
    SparseMatrix,
    isinstance_validator(sparse.csr_matrix),
]
type DIAMatrix = Annotated[
    SparseMatrix,
    isinstance_validator(sparse.dia_matrix),
]
type DOKMatrix = Annotated[
    SparseMatrix,
    isinstance_validator(sparse.dok_matrix),
]
type LILMatrix = Annotated[
    SparseMatrix,
    isinstance_validator(sparse.lil_matrix),
]

### scipy.stats

class RVHistogram(rv_histogram):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        def _validate(value: object):
            if isinstance(value, rv_histogram):
                return value

            try:
                value = rv_histogram(value)
            except Exception as exc:
                raise PydanticCustomError(
                    "validation_error",
                    f"Failed to coerce value of type {type(value).__name__} "
                    f"to scipy.stats.rv_histogram"
                ) from exc
        return no_info_plain_validator_function(_validate)

class RVContinuous(rv_continuous):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(rv_continuous)
        )

class RVContinuousFrozen(rv_continuous_frozen):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(rv_continuous_frozen)
        )