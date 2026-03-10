__all__ = ['csr_matrix_']

from scipy.sparse import csr_matrix
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class csr_matrix_(csr_matrix):
    """
    scipy.sparse.csr_matrix
    """
    @classmethod
    def _validate(cls, value: object) -> csr_matrix:
        if not isinstance(value, csr_matrix):
            msg = f'Expected a csr_matrix, got {type(value).__name__}'
            raise PydanticCustomError('csr_matrix_type_error', msg)
        return value
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)