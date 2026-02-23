class AbsolutePathLike:
    """
    Type hint for validating absolute existing paths with pydantic.
    """
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        
        def validate(value):
            from . import utils

            value = utils._coerce_to_path(value)
            utils._check_is_absolute(value)
            utils._check_path_exists(value)
            
            return value
        
        return core_schema.no_info_plain_validator_function(validate)
    
class NewAbsolutePathLike:
    """
    Type hint for validating absolute paths that do not exist with pydantic.
    """
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        
        def validate(value):
            from . import utils

            value = utils._coerce_to_path(value)
            utils._check_is_absolute(value)
            utils._check_path_doesnt_exist(value)
            
            return value
        
        return core_schema.no_info_plain_validator_function(validate)
    
class RelativePathLike:
    """
    Type hint for validating relative existing paths with pydantic.
    """
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        
        def validate(value):
            from . import utils

            value = utils._coerce_to_path(value)
            utils._check_is_relative(value)
            
            return value
        
        return core_schema.no_info_plain_validator_function(validate)