class CoordBounds:
    """
    Type hint for validating coordinate bounds tuples with pydantic.
    Each tuple must contain exactly 2 elements representing the lower
    and upper bounds respectively.
    """
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        
        def validate(value):
            from pydantic_core import PydanticCustomError

            if not isinstance(value, tuple):
                msg = "Value must be a 'tuple', not '{}'!"
                raise PydanticCustomError('validation_error', msg)
            
            if not len(value) == 2:
                msg = "Tuple must only contain 2 values, not '{}'!"
                raise PydanticCustomError('validation_error', msg)
            
            if not all(isinstance(_, float) for _ in value):
                msg = "Tuple elements must be of type 'float'!"
                raise PydanticCustomError('validation_error', msg)
            
            if not (value[0] < value[1]): 
                msg = "Tuple must be 'increasing'!"
                raise PydanticCustomError('validation_error', msg)

            return value
        
        return core_schema.no_info_plain_validator_function(validate)

class AstropyBounds:
    """
    Type hint for validating coordinate bounds tuples with pydantic.
    Each tuple must contain exactly 2 elements representing the lower
    and upper bounds respectively.
    """
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        
        def validate(value):
            from pydantic_core import PydanticCustomError

            if not isinstance(value, tuple):
                msg = "Value must be a 'tuple', not '{}'!"
                raise PydanticCustomError('validation_error', msg)
            
            if not len(value) == 2:
                msg = "Tuple must only contain 2 values, not '{}'!"
                raise PydanticCustomError('validation_error', msg)
            
            for _ in value:
                if _ is None: continue
                if not isinstance(_, float):
                    msg = "Tuple elements must be of type 'float' or 'None'!"
                    raise PydanticCustomError('validation_error', msg)
                
            if (None not in value) and not (value[0] < value[1]): 
                msg = "Tuple must be 'increasing'!"
                raise PydanticCustomError('validation_error', msg)

            return value
        
        return core_schema.no_info_plain_validator_function(validate)