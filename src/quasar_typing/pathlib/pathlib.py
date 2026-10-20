"""Path type aliases with validators."""

from pathlib import Path
from typing import Annotated

from . import validators

type AnyPath = Annotated[Path, validators.coerce]
type NewPath = Annotated[AnyPath, validators.doesnt_exist]
type ExistingPath = Annotated[AnyPath, validators.exists]

### File paths

type AnyFilePath = Annotated[AnyPath, validators.has_suffix]
type NewFilePath = Annotated[NewPath, validators.has_suffix]
type FilePath = Annotated[ExistingPath, validators.is_file]

### Directory paths


type AnyDirPath = Annotated[AnyPath, validators.has_no_suffix]
type NewDirPath = Annotated[NewPath, validators.has_no_suffix]
type DirPath = Annotated[ExistingPath, validators.is_dir]

### CSV

type AnyCSVPath = Annotated[AnyFilePath, validators.is_csv]
type NewCSVPath = Annotated[NewFilePath, validators.is_csv]
type CSVPath = Annotated[FilePath, validators.is_csv]

### ASCII

type AnyASCIIPath = Annotated[AnyFilePath, validators.is_ascii]
type NewASCIIPath = Annotated[NewFilePath, validators.is_ascii]
type ASCIIPath = Annotated[FilePath, validators.is_ascii]

### FITS

type AnyFITSPath = Annotated[AnyFilePath, validators.is_fits]
type NewFITSPath = Annotated[NewFilePath, validators.is_fits]
type FITSPath = Annotated[FilePath, validators.is_fits]

### JSON


type AnyJSONPath = Annotated[AnyFilePath, validators.is_json]
type NewJSONPath = Annotated[NewFilePath, validators.is_json]
type JSONPath = Annotated[FilePath, validators.is_json]

### YAML

type AnyYAMLPath = Annotated[AnyFilePath, validators.is_yaml]
type NewYAMLPath = Annotated[NewFilePath, validators.is_yaml]
type YAMLPath = Annotated[FilePath, validators.is_yaml]

### TOML

type AnyTOMLPath = Annotated[AnyFilePath, validators.is_toml]
type NewTOMLPath = Annotated[NewFilePath, validators.is_toml]
type TOMLPath = Annotated[FilePath, validators.is_toml]

### TOON

type AnyTOONPath = Annotated[AnyFilePath, validators.is_toon]
type NewTOONPath = Annotated[NewFilePath, validators.is_toon]
type TOONPath = Annotated[FilePath, validators.is_toon]

### PKL

type AnyPKLPath = Annotated[AnyFilePath, validators.is_pkl]
type NewPKLPath = Annotated[NewFilePath, validators.is_pkl]
type PKLPath = Annotated[FilePath, validators.is_pkl]

### HDF5

type AnyHDF5Path = Annotated[AnyFilePath, validators.is_hdf5]
type NewHDF5Path = Annotated[NewFilePath, validators.is_hdf5]
type HDF5Path = Annotated[FilePath, validators.is_hdf5]

### LOG

type AnyLogPath = Annotated[AnyFilePath, validators.is_log]
type NewLogPath = Annotated[NewFilePath, validators.is_log]
type LogPath = Annotated[FilePath, validators.is_log]
