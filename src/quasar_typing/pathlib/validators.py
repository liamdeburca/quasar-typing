from pathlib import Path
from typing import Any

from ..utils import after_validator_decorator, before_validator_decorator


@before_validator_decorator
def coerce(value: Any) -> Path:
    from pydantic_core import PydanticCustomError
    try:
        return Path(value).expanduser().resolve()
    except TypeError:
        raise PydanticCustomError(
            "validation_error",
            "Value cannot be converted to a Path"
        )


@after_validator_decorator
def exists(p: Path) -> Path:
    from pydantic_core import PydanticCustomError
    if not p.exists():
        raise PydanticCustomError(
            "validation_error",
            "Path does not exist"
        )
    return p


@after_validator_decorator
def doesnt_exist(p: Path) -> Path:
    from pydantic_core import PydanticCustomError
    if p.exists():
        raise PydanticCustomError(
            "validation_error",
            "Path exists"
        )
    return p



@after_validator_decorator
def has_suffix(p: Path) -> Path:
    from pydantic_core import PydanticCustomError
    if p.suffix == "":
        raise PydanticCustomError(
            "validation_error",
            "Path does not have a suffix"
        )
    return p


@after_validator_decorator
def is_file(p: Path) -> Path:
    from pydantic_core import PydanticCustomError
    if not p.is_file():
        raise PydanticCustomError(
            "validation_error",
            "Path is not a file"
        )
    return p


@after_validator_decorator
def has_no_suffix(p: Path) -> Path:
    from pydantic_core import PydanticCustomError
    if p.suffix != "":
        raise PydanticCustomError(
            "validation_error",
            "Path has a suffix"
        )
    return p


@after_validator_decorator
def is_dir(p: Path) -> Path:
    from pydantic_core import PydanticCustomError
    if not p.is_dir():
        raise PydanticCustomError(
            "validation_error",
            "Path is not a directory"
        )
    return p


@after_validator_decorator
def is_csv(p: Path) -> Path:
    from pydantic_core import PydanticCustomError
    if p.suffix != ".csv":
        raise PydanticCustomError(
            "validation_error",
            "Path is not a CSV file"
        )
    return p

@after_validator_decorator
def is_ascii(p: Path) -> Path:
    from pydantic_core import PydanticCustomError
    if p.suffix != ".asc":
        raise PydanticCustomError(
            "validation_error",
            "Path is not an ASCII file"
        )
    return p


@after_validator_decorator
def is_fits(p: Path) -> Path:
    from pydantic_core import PydanticCustomError
    if p.suffix != ".fits":
        raise PydanticCustomError(
            "validation_error",
            "Path is not a FITS file"
        )
    return p


@after_validator_decorator
def is_json(p: Path) -> Path:
    from pydantic_core import PydanticCustomError
    if p.suffix != ".json":
        raise PydanticCustomError(
            "validation_error",
            "Path is not a JSON file"
        )
    return p


@after_validator_decorator
def is_yaml(p: Path) -> Path:
    from pydantic_core import PydanticCustomError
    if p.suffix not in {".yaml", ".yml"}:
        raise PydanticCustomError(
            "validation_error",
            "Path is not a YAML file"
        )
    return p



@after_validator_decorator
def is_toml(p: Path) -> Path:
    from pydantic_core import PydanticCustomError
    if p.suffix != ".toml":
        raise PydanticCustomError(
            "validation_error",
            "Path is not a TOML file"
        )
    return p



@after_validator_decorator
def is_toon(p: Path) -> Path:
    from pydantic_core import PydanticCustomError
    if p.suffix != ".toon":
        raise PydanticCustomError(
            "validation_error",
            "Path is not a TOON file"
        )
    return p


@after_validator_decorator
def is_pkl(p: Path) -> Path:
    from pydantic_core import PydanticCustomError
    if p.suffix != ".pkl":
        raise PydanticCustomError(
            "validation_error",
            "Path is not a PKL file"
        )
    return p



@after_validator_decorator
def is_hdf5(p: Path) -> Path:
    from pydantic_core import PydanticCustomError
    if p.suffix not in {".h5", ".hdf5"}:
        raise PydanticCustomError(
            "validation_error",
            "Path is not an HDF5 file"
        )
    return p


@after_validator_decorator
def is_log(p: Path) -> Path:
    from pydantic_core import PydanticCustomError
    if p.suffix != ".log":
        raise PydanticCustomError(
            "validation_error",
            "Path is not a LOG file"
        )
    return p