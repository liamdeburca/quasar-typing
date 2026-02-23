from numpy import ndarray

class FloatArray(ndarray):
    """
    Type hint for validating any NumPy array_like of floats with pydantic.
    """
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema

        def validate(value: object) -> object:
            from . import utils

            utils._check_is_ndarray(value)
            utils._check_is_float_array(value)

            return value
            
        return core_schema.no_info_plain_validator_function(validate)

class FloatVector(ndarray):
    """
    Type hint for validating a 1D NumPy array_like of floats with pydantic.
    """
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema

        def validate(value: object) -> object:
            from . import utils

            utils._check_is_ndarray(value)
            utils._check_is_float_array(value)
            utils._check_ndim(value, 1)

            return value
            
        return core_schema.no_info_plain_validator_function(validate)
    
class FloatMatrix(ndarray):
    """
    Type hint for validating a 2D NumPy array_like of floats with pydantic.
    """
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema

        def validate(value: object) -> object:
            from . import utils

            utils._check_is_ndarray(value)
            utils._check_is_float_array(value)
            utils._check_ndim(value, 2)

            return value
            
        return core_schema.no_info_plain_validator_function(validate)
    
class FloatCube(ndarray):
    """
    Type hint for validating a 3D NumPy array_like of floats with pydantic.
    """
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema

        def validate(value: object) -> object:
            from . import utils

            utils._check_is_ndarray(value)
            utils._check_is_float_array(value)
            utils._check_ndim(value, 3)

            return value
            
        return core_schema.no_info_plain_validator_function(validate)
    
class FittableFloatVector(ndarray):
    """
    Type hint for validating a NumPy array_like of floats that is compatible
    with AstroPy's FittableModel with pydantic.
    """
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema

        def validate(value: object) -> object:
            from . import utils
            
            utils._check_is_ndarray(value)
            utils._check_is_float_array(value)
            utils._check_contains_elements(value)
            utils._check_ndim(value, 1)
            utils._check_is_pure(value)

            return value
            
        return core_schema.no_info_plain_validator_function(validate)