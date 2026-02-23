class AbsoluteFITSLike:
    """
    Type hint for validating absolute existing FITS files with pydantic.
    """
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        
        def validate(value):
            from . import utils

            value = utils._coerce_to_path(value)
            utils._check_is_absolute(value)
            utils._check_path_exists(value)
            utils._check_extension(value, 'fits')

            return value
        
        return core_schema.no_info_plain_validator_function(validate)
    
class NewAbsoluteFITSLike:
    """
    Type hint for validating absolute FITS files that do not exist with pydantic.
    """
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        
        def validate(value):
            from . import utils

            value = utils._coerce_to_path(value)
            utils._check_is_absolute(value)
            utils._check_path_doesnt_exist(value)
            utils._check_extension(value, 'fits')

            return value
        
        return core_schema.no_info_plain_validator_function(validate)
    
class RelativeFITSLike:
    """
    Type hint for validating relative existing FITS files with pydantic.
    """
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        
        def validate(value):
            from . import utils

            value = utils._coerce_to_path(value)
            utils._check_is_relative(value)
            utils._check_extension(value, 'fits')

            return value
        
        return core_schema.no_info_plain_validator_function(validate)