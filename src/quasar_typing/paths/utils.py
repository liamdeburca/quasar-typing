from pathlib import Path
from pydantic_core import PydanticCustomError

def _coerce_to_path(value: str | Path) -> Path:
    if not isinstance(value, (str, Path)):
        msg = "Expected str or Path, got {}".format(
            type(value).__name__,
        )
        raise PydanticCustomError('validation_error', msg)

    return Path(value)

def _check_is_absolute(path: Path) -> None:
    if not path.is_absolute():
        raise PydanticCustomError('validation_error', "Path must be absolute.")
    
def _check_is_relative(path: Path) -> None:
    if path.is_absolute():
        raise PydanticCustomError('validation_error', "Path must be relative.")
    
def _check_path_exists(path: Path) -> None:
    if not path.exists():
        raise PydanticCustomError('validation_error', "Path must exist.")
    
def _check_path_doesnt_exist(path: Path) -> None:
    if path.exists():
        raise PydanticCustomError('validation_error', "Path must not exist.")
    
def _check_path_is_file(path: Path) -> None:
    if not path.is_file():
        raise PydanticCustomError('validation_error', "Path must be a file.")
    
def _check_path_is_dir(path: Path) -> None:
    if not path.is_dir():
        raise PydanticCustomError('validation_error', "Path must be a directory.")
    
def _check_extension(path: Path, ext: str) -> None:
    if path.suffix.removeprefix('.') != ext.lower():
        raise PydanticCustomError(
            'validation_error',
            f"Path must have extension '{ext}'.",
        )