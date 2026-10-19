from pathlib import Path
from typing import Annotated, Any

from pydantic_core import PydanticCustomError

from .utils import after_validator_decorator, before_validator_decorator


@before_validator_decorator
def coerce(value: Any) -> Path:
    try:
        return Path(value).expanduser().resolve()
    except TypeError:
        raise PydanticCustomError(
            "validation_error",
            "Value cannot be converted to a Path"
        )


@after_validator_decorator
def exists(p: Path) -> Path:
    if not p.exists():
        raise PydanticCustomError(
            "validation_error",
            "Path does not exist"
        )
    return p


@after_validator_decorator
def doesnt_exist(p: Path) -> Path:
    if p.exists():
        raise PydanticCustomError(
            "validation_error",
            "Path exists"
        )
    return p


type AnyPath = Annotated[Path, coerce]
type NewPath = Annotated[AnyPath, doesnt_exist]
type ExistingPath = Annotated[AnyPath, exists]

### File paths


@after_validator_decorator
def has_suffix(p: Path) -> Path:
    if p.suffix == "":
        raise PydanticCustomError(
            "validation_error",
            "Path does not have a suffix"
        )
    return p


@after_validator_decorator
def is_file(p: Path) -> Path:
    if not p.is_file():
        raise PydanticCustomError(
            "validation_error",
            "Path is not a file"
        )
    return p


type AnyFilePath = Annotated[AnyPath, has_suffix]
type NewFilePath = Annotated[NewPath, has_suffix]
type FilePath = Annotated[ExistingPath, is_file]

### Directory paths


@after_validator_decorator
def has_no_suffix(p: Path) -> Path:
    if p.suffix != "":
        raise PydanticCustomError(
            "validation_error",
            "Path has a suffix"
        )
    return p


@after_validator_decorator
def is_dir(p: Path) -> Path:
    if not p.is_dir():
        raise PydanticCustomError(
            "validation_error",
            "Path is not a directory"
        )
    return p


type AnyDirPath = Annotated[AnyPath, has_no_suffix]
type NewDirPath = Annotated[NewPath, has_no_suffix]
type DirPath = Annotated[ExistingPath, is_dir]

### CSV


@after_validator_decorator
def is_csv(p: Path) -> Path:
    if p.suffix != ".csv":
        raise PydanticCustomError(
            "validation_error",
            "Path is not a CSV file"
        )
    return p


type AnyCSVPath = Annotated[AnyFilePath, is_csv]
type NewCSVPath = Annotated[NewFilePath, is_csv]
type CSVPath = Annotated[FilePath, is_csv]

### ASCII


@after_validator_decorator
def is_ascii(p: Path) -> Path:
    if p.suffix != ".asc":
        raise PydanticCustomError(
            "validation_error",
            "Path is not an ASCII file"
        )
    return p


type AnyASCIIPath = Annotated[AnyFilePath, is_ascii]
type NewASCIIPath = Annotated[NewFilePath, is_ascii]
type ASCIIPath = Annotated[FilePath, is_ascii]

### FITS


@after_validator_decorator
def is_fits(p: Path) -> Path:
    if p.suffix != ".fits":
        raise PydanticCustomError(
            "validation_error",
            "Path is not a FITS file"
        )
    return p


type AnyFITSPath = Annotated[AnyFilePath, is_fits]
type NewFITSPath = Annotated[NewFilePath, is_fits]
type FITSPath = Annotated[FilePath, is_fits]

### JSON


@after_validator_decorator
def is_json(p: Path) -> Path:
    if p.suffix != ".json":
        raise PydanticCustomError(
            "validation_error",
            "Path is not a JSON file"
        )
    return p


type AnyJSONPath = Annotated[AnyFilePath, is_json]
type NewJSONPath = Annotated[NewFilePath, is_json]
type JSONPath = Annotated[FilePath, is_json]

### YAML


@after_validator_decorator
def is_yaml(p: Path) -> Path:
    if p.suffix not in {".yaml", ".yml"}:
        raise PydanticCustomError(
            "validation_error",
            "Path is not a YAML file"
        )
    return p


type AnyYAMLPath = Annotated[AnyFilePath, is_yaml]
type NewYAMLPath = Annotated[NewFilePath, is_yaml]
type YAMLPath = Annotated[FilePath, is_yaml]

### TOML


@after_validator_decorator
def is_toml(p: Path) -> Path:
    if p.suffix != ".toml":
        raise PydanticCustomError(
            "validation_error",
            "Path is not a TOML file"
        )
    return p


type AnyTOMLPath = Annotated[AnyFilePath, is_toml]
type NewTOMLPath = Annotated[NewFilePath, is_toml]
type TOMLPath = Annotated[FilePath, is_toml]

### TOON


@after_validator_decorator
def is_toon(p: Path) -> Path:
    if p.suffix != ".toon":
        raise PydanticCustomError(
            "validation_error",
            "Path is not a TOON file"
        )
    return p


type AnyTOONPath = Annotated[AnyFilePath, is_toon]
type NewTOONPath = Annotated[NewFilePath, is_toon]
type TOONPath = Annotated[FilePath, is_toon]

### PKL


@after_validator_decorator
def is_pkl(p: Path) -> Path:
    if p.suffix != ".pkl":
        raise PydanticCustomError(
            "validation_error",
            "Path is not a PKL file"
        )
    return p


type AnyPKLPath = Annotated[AnyFilePath, is_pkl]
type NewPKLPath = Annotated[NewFilePath, is_pkl]
type PKLPath = Annotated[FilePath, is_pkl]

### HDF5


@after_validator_decorator
def is_hdf5(p: Path) -> Path:
    if p.suffix not in {".h5", ".hdf5"}:
        raise PydanticCustomError(
            "validation_error",
            "Path is not an HDF5 file"
        )
    return p


type AnyHDF5Path = Annotated[AnyFilePath, is_hdf5]
type NewHDF5Path = Annotated[NewFilePath, is_hdf5]
type HDF5Path = Annotated[FilePath, is_hdf5]

### LOG


@after_validator_decorator
def is_log(p: Path) -> Path:
    if p.suffix != ".log":
        raise PydanticCustomError(
            "validation_error",
            "Path is not a LOG file"
        )
    return p


type AnyLogPath = Annotated[AnyFilePath, is_log]
type NewLogPath = Annotated[NewFilePath, is_log]
type LogPath = Annotated[FilePath, is_log]
