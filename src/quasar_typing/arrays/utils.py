def _check_is_ndarray(value) -> None:
    from pydantic_core import PydanticCustomError
    from numpy import ndarray

    if not isinstance(value, ndarray):
        msg = "Value must be a 'numpy.array', not '{}'!"\
            .format(type(value).__name__)
        raise PydanticCustomError('validation_error', msg)
    
def _check_is_float_array(value) -> None:
    from pydantic_core import PydanticCustomError
    from numpy import issubdtype, float_

    if not issubdtype(value.dtype, float_):
        msg = "Array elements must be of type 'float', not '{}'!"\
            .format(value.dtype)
        raise PydanticCustomError('validation_error', msg)
    
def _check_is_int_array(value) -> None:
    from pydantic_core import PydanticCustomError
    from numpy import issubdtype, int_

    if not issubdtype(value.dtype, int_):
        msg = "Array elements must be of type 'int', not '{}'!"\
            .format(value.dtype)
        raise PydanticCustomError('validation_error', msg)
    
def _check_is_bool_array(value) -> None:
    from pydantic_core import PydanticCustomError
    from numpy import issubdtype, bool_

    if not issubdtype(value.dtype, bool_):
        msg = "Array elements must be of type 'bool', not '{}'!"\
            .format(value.dtype)
        raise PydanticCustomError('validation_error', msg)
    
def _check_ndim(value, ndim: int) -> None:
    from pydantic_core import PydanticCustomError

    if value.ndim != ndim:
        msg = "Array must have '{}' dimensions, not '{}'!"\
            .format(ndim, value.ndim)                        
        raise PydanticCustomError('validation_error', msg)

def _check_is_pure(value) -> None:
    from pydantic_core import PydanticCustomError
    from numpy import isnan

    if isnan(value).any():
        msg = "Array must not contain NaN values"
        raise PydanticCustomError('validation_error', msg)
    
def _check_contains_elements(value) -> None:
    from pydantic_core import PydanticCustomError

    if value.size == 0:
        msg = "Array must contain elements!"
        raise PydanticCustomError('validation_error', msg)