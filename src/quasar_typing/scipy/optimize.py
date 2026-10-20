__all__ = ["OptimizeResultType"]
import math
from typing import Literal, Self

from pydantic import validate_call
from scipy.optimize import OptimizeResult

from quasar_typing.numpy import FloatMatrix, FloatVector


class OptimizeResultType(OptimizeResult):
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
    def fromFitInfo(cls, fit_info: OptimizeResult) -> Self:
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
        from pydantic_core import PydanticCustomError
        
        if isinstance(value, cls):
            return value

        if isinstance(value, OptimizeResult):
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
        from pydantic_core.core_schema import no_info_plain_validator_function
        return no_info_plain_validator_function(cls._validate)

    @property
    def dof(self) -> int:
        return self.fun.size - self.x.size

    @property
    def chi2(self) -> float:
        return (self.fun * self.fun).sum()

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