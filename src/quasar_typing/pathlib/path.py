from typing import Literal
from pathlib import Path
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class Path_(Path):
    """
    pathlib.Path
    """
    _absolute: bool | None = None
    _exists: bool | None = None
    _file_type: Literal['file', 'directory'] | str | None = None

    @classmethod
    def _validate(cls, value: object) -> Path:
        if isinstance(value, str):
            value = Path(value)
        elif not isinstance(value, Path):
            msg = f"Expected a path-like object, got {type(value).__name__}"
            raise PydanticCustomError("validation_error", msg)

        if cls._absolute is not None:
            if cls._absolute and not value.is_absolute():
                msg = f"Expected an absolute path, got {value}"
                raise PydanticCustomError("validation_error", msg)
            if not cls._absolute and value.is_absolute():
                msg = f"Expected a relative path, got {value}"
                raise PydanticCustomError("validation_error", msg)

        if cls._exists is not None:
            if cls._exists and not value.exists():
                msg = f"Expected an existing path, got {value}"
                raise PydanticCustomError("validation_error", msg)
            if not cls._exists and value.exists():
                msg = f"Expected a non-existing path, got {value}"
                raise PydanticCustomError("validation_error", msg)

        match cls._file_type:
            case None:
                pass
            case 'directory':
                is_dir = value.is_dir() if value.exists() else not value.suffix
                if not is_dir:
                    msg = f"Expected a directory path, got {value}"
                    raise PydanticCustomError("validation_error", msg)
            case 'file':
                is_file = value.is_file() if value.exists() else value.suffix
                if not is_file:
                    msg = f"Expected a file path, got {value}"
                    raise PydanticCustomError("validation_error", msg)
            case _:
                if not value.suffix == cls._file_type:
                    msg = f"Expected a path with extension {cls._file_type}, " \
                        f"got {value.name}"
                    raise PydanticCustomError("validation_error", msg)
        
        return Path(value)
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)
    
    @classmethod
    def __class_getitem__(cls, specs) -> type['Path_']:
        class TypedPath_(Path_):
            _absolute: bool | None = specs[1]
            _exists: bool | None = specs[2]
            _file_type: Literal['file', 'directory'] | str | None = specs[3]

        TypedPath_.__doc__ = specs[0]

        return TypedPath_