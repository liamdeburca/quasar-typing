from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class AstropyBounds(tuple[float | None, float | None]):
    """
    2-tuple of 'float' or 'None'
    """
    @classmethod
    def _validate(cls, value: object) -> tuple[float | None, float | None]:
        if not isinstance(value, tuple):
            msg = f"Value must be a 'tuple', not '{type(value).__name__}'!"
            raise PydanticCustomError('validation_error', msg)
        
        if not len(value) == 2:
            msg = f"Tuple must only contain 2 values, not '{len(value)}'!"
            raise PydanticCustomError('validation_error', msg)
        
        if all(val is None for val in value):
            msg = "Tuple cannot contain only 'None' values!"
            raise PydanticCustomError('validation_error', msg)
        
        for val in value:
            if val is None: continue
            if not isinstance(val, float):
                msg = "Tuple elements must be of type 'float' or 'None'!"
                raise PydanticCustomError('validation_error', msg)
        
        if (None not in value) and not (value[0] < value[1]):
            msg = "Tuple must be 'increasing'!"
            raise PydanticCustomError('validation_error', msg)

        return value
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)