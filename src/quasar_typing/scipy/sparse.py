__all__ = [
    "CSRArray",
    "CSRMatrix",
    "DIAArray",
    "DIAMatrix",
    "SparseArray",
    "SparseMatrix",
]
from typing import Annotated

from scipy.sparse import (
    csr_array,
    csr_matrix,
    dia_array,
    dia_matrix,
    sparray,
    spmatrix,
)

from ..utils import isinstance_func, isinstance_validator

### scipy.optimize.OptimizeResult


# Arrays

class SparseArray(sparray):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core.core_schema import no_info_plain_validator_function
        return no_info_plain_validator_function(
            isinstance_func(sparray)
        )

type CSRArray = Annotated[
    SparseArray,
    isinstance_validator(csr_array),
]
type DIAArray = Annotated[
    SparseArray,
    isinstance_validator(dia_array),
]

# Matrices

class SparseMatrix(spmatrix):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core.core_schema import no_info_plain_validator_function
        return no_info_plain_validator_function(
            isinstance_func(spmatrix)
        )
    
type CSRMatrix = Annotated[
    SparseMatrix,
    isinstance_validator(csr_matrix),
]
type DIAMatrix = Annotated[
    SparseMatrix,
    isinstance_validator(dia_matrix),
]