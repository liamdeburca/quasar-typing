from typing import Self
from pathlib import Path
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class Path_(Path):
    """
    Type hint for validating paths with pydantic.
    """
    @classmethod
    def _validate(cls, value: object) -> Path:
        if not isinstance(value, (Path, str)):
            msg = f"Expected a path-like object, got {type(value).__name__}"
            raise PydanticCustomError("validation_error", msg)
        
        return Path(value)
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)
    
    @classmethod
    def __class_getitem__(cls, specs) -> Self:
        if not isinstance(specs, tuple):
            specs = (specs,)

        doc: str = specs[0]
        absolute: bool = specs[1] if len(specs) > 1 else None
        exists: bool = specs[2] if len(specs) > 2 else True
        ftype: str = specs[3] if len(specs) > 3 else None

        class TypedPath_(Path_):
            @classmethod
            def _validate(cls, value: object) -> Path:
                path = super()._validate(value)

                if absolute is not None:
                    if absolute and not path.is_absolute():
                        msg = f"Expected an absolute path, got {path}"
                        raise PydanticCustomError("validation_error", msg)
                    if not absolute and path.is_absolute():
                        msg = f"Expected a relative path, got {path}"
                        raise PydanticCustomError("validation_error", msg)
                
                if exists is not None:
                    if exists and not path.exists():
                        msg = f"Expected an existing path, got {path}"
                        raise PydanticCustomError("validation_error", msg)
                    if not exists and path.exists():
                        msg = f"Expected a non-existing path, got {path}"
                        raise PydanticCustomError("validation_error", msg)
                    
                if ftype is not None:
                    if ftype == 'file' and not path.is_file():
                        msg = f"Expected a file path, got {path}"
                        raise PydanticCustomError("validation_error", msg)
                    if ftype == 'dir' and not path.is_dir():
                        msg = f"Expected a directory path, got {path}"
                        raise PydanticCustomError("validation_error", msg)
                    if not path.name.endswith(ftype):
                        msg = "Expected a path with extension {}, for {}" \
                            .format(ftype, path.name)
                        raise PydanticCustomError("validation_error", msg)
                    
                return path
            
        TypedPath_.__doc__ = doc
            
        return TypedPath_