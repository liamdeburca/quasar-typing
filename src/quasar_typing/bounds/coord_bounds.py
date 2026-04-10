from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class CoordBounds(tuple[float, float]):
    """
    2-tuple of 'float' (must be increasing)
    """
    @classmethod
    def _validate(cls, value: object) -> tuple[float, float]:
        if not isinstance(value, tuple):
            msg = f"Value must be a 'tuple', not '{type(value).__name__}'!"
            raise PydanticCustomError('validation_error', msg)
        
        if not len(value) == 2:
            msg = f"Tuple must only contain 2 values, not '{len(value)}'!"
            raise PydanticCustomError('validation_error', msg)
        
        if not all(isinstance(_, (float, int)) for _ in value):
            msg = "Tuple elements must be of type 'float'!"
            raise PydanticCustomError('validation_error', msg)
        
        if not (value[0] < value[1]): 
            msg = "Tuple must be 'increasing'!"
            raise PydanticCustomError('validation_error', msg)

        return (float(value[0]), float(value[1]))
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)