from pathlib import Path

import pytest
from pydantic import TypeAdapter, ValidationError

from quasar_typing.pathlib import (
    AnyDirPath,
    AnyFilePath,
    AnyPath,
    CSVPath,
    DirPath,
    ExistingPath,
    FilePath,
    JSONPath,
    NewPath,
    ASCIIPath,
    FITSPath,
    YAMLPath,
    TOMLPath,
    TOONPath,
    PKLPath,
    HDF5Path,
    LogPath,
)


class TestAnyPath:
    def test_positive(self, testdata_dir: Path):
        ta = TypeAdapter(AnyPath)
        # should accept an existing path
        p = testdata_dir / "sample.csv"
        out = ta.validate_python(str(p))
        assert isinstance(out, Path)

    def test_negative(self, testdata_dir: Path):
        ta = TypeAdapter(AnyPath)
        # passing a non-pathable object should raise
        with pytest.raises(ValidationError):
            ta.validate_python(123)


class TestNewPath:
    def test_positive(self, testdata_dir: Path):
        ta = TypeAdapter(NewPath)
        # should accept a new (non-existing) path
        p = testdata_dir / "does_not_exist.tmp"
        out = ta.validate_python(str(p))
        assert isinstance(out, Path)

    def test_negative(self, testdata_dir: Path):
        ta = TypeAdapter(NewPath)
        p = testdata_dir / "sample.csv"
        with pytest.raises(ValidationError):
            ta.validate_python(str(p))


class TestExistingPath:
    def test_positive(self, testdata_dir: Path):
        ta = TypeAdapter(ExistingPath)
        p = testdata_dir / "sample.csv"
        out = ta.validate_python(str(p))
        assert isinstance(out, Path)

    def test_negative(self, testdata_dir: Path):
        ta = TypeAdapter(ExistingPath)
        p = testdata_dir / "does_not_exist.tmp"
        with pytest.raises(ValidationError):
            ta.validate_python(str(p))


class TestAnyFilePath:
    def test_positive(self, testdata_dir: Path):
        ta = TypeAdapter(AnyFilePath)
        p = testdata_dir / "sample.csv"
        out = ta.validate_python(str(p))
        assert isinstance(out, Path)

    def test_negative(self, testdata_dir: Path):
        ta = TypeAdapter(AnyFilePath)
        # directory should fail
        p = testdata_dir / "dir1"
        with pytest.raises(ValidationError):
            ta.validate_python(str(p))


class TestFilePath:
    def test_positive(self, testdata_dir: Path):
        ta = TypeAdapter(FilePath)
        p = testdata_dir / "sample.csv"
        out = ta.validate_python(str(p))
        assert isinstance(out, Path)

    def test_negative(self, testdata_dir: Path):
        ta = TypeAdapter(FilePath)
        p = testdata_dir / "dir1"
        with pytest.raises(ValidationError):
            ta.validate_python(str(p))


class TestAnyDirPath:
    def test_positive(self, testdata_dir: Path):
        ta = TypeAdapter(AnyDirPath)
        p = testdata_dir / "dir1"
        out = ta.validate_python(str(p))
        assert isinstance(out, Path)

    def test_negative(self, testdata_dir: Path):
        ta = TypeAdapter(AnyDirPath)
        p = testdata_dir / "sample.csv"
        with pytest.raises(ValidationError):
            ta.validate_python(str(p))


class TestAbsoluteDirPath:
    def test_positive(self, testdata_dir: Path):
        ta = TypeAdapter(DirPath)
        p = testdata_dir / "dir1"
        out = ta.validate_python(str(p))
        assert isinstance(out, Path)

    def test_negative(self, testdata_dir: Path):
        ta = TypeAdapter(DirPath)
        p = testdata_dir / "sample.csv"
        with pytest.raises(ValidationError):
            ta.validate_python(str(p))


class TestCSVPath:
    def test_positive(self, testdata_dir: Path):
        ta = TypeAdapter(CSVPath)
        p = testdata_dir / "sample.csv"
        out = ta.validate_python(str(p))
        assert isinstance(out, Path)

    def test_negative(self, testdata_dir: Path):
        ta = TypeAdapter(CSVPath)
        p = testdata_dir / "sample.json"
        with pytest.raises(ValidationError):
            ta.validate_python(str(p))


class TestJSONPath:
    def test_positive(self, testdata_dir: Path):
        ta = TypeAdapter(JSONPath)
        p = testdata_dir / "sample.json"
        out = ta.validate_python(str(p))
        assert isinstance(out, Path)

    def test_negative(self, testdata_dir: Path):
        ta = TypeAdapter(JSONPath)
        p = testdata_dir / "sample.csv"
        with pytest.raises(ValidationError):
            ta.validate_python(str(p))


class TestASCIIPath:
    def test_positive(self, testdata_dir: Path):
        ta = TypeAdapter(ASCIIPath)
        p = testdata_dir / "sample.asc"
        out = ta.validate_python(str(p))
        assert isinstance(out, Path)

    def test_negative(self, testdata_dir: Path):
        ta = TypeAdapter(ASCIIPath)
        p = testdata_dir / "sample.csv"
        with pytest.raises(ValidationError):
            ta.validate_python(str(p))


class TestFITSPath:
    def test_positive(self, testdata_dir: Path):
        ta = TypeAdapter(FITSPath)
        p = testdata_dir / "sample.fits"
        out = ta.validate_python(str(p))
        assert isinstance(out, Path)

    def test_negative(self, testdata_dir: Path):
        ta = TypeAdapter(FITSPath)
        p = testdata_dir / "sample.csv"
        with pytest.raises(ValidationError):
            ta.validate_python(str(p))


class TestYAMLPath:
    def test_positive(self, testdata_dir: Path):
        ta = TypeAdapter(YAMLPath)
        p = testdata_dir / "sample.yaml"
        out = ta.validate_python(str(p))
        assert isinstance(out, Path)

    def test_negative(self, testdata_dir: Path):
        ta = TypeAdapter(YAMLPath)
        p = testdata_dir / "sample.csv"
        with pytest.raises(ValidationError):
            ta.validate_python(str(p))


class TestTOMLPath:
    def test_positive(self, testdata_dir: Path):
        ta = TypeAdapter(TOMLPath)
        p = testdata_dir / "sample.toml"
        out = ta.validate_python(str(p))
        assert isinstance(out, Path)

    def test_negative(self, testdata_dir: Path):
        ta = TypeAdapter(TOMLPath)
        p = testdata_dir / "sample.csv"
        with pytest.raises(ValidationError):
            ta.validate_python(str(p))


class TestTOONPath:
    def test_positive(self, testdata_dir: Path):
        ta = TypeAdapter(TOONPath)
        p = testdata_dir / "sample.toon"
        out = ta.validate_python(str(p))
        assert isinstance(out, Path)

    def test_negative(self, testdata_dir: Path):
        ta = TypeAdapter(TOONPath)
        p = testdata_dir / "sample.csv"
        with pytest.raises(ValidationError):
            ta.validate_python(str(p))


class TestPKLPath:
    def test_positive(self, testdata_dir: Path):
        ta = TypeAdapter(PKLPath)
        p = testdata_dir / "sample.pkl"
        out = ta.validate_python(str(p))
        assert isinstance(out, Path)

    def test_negative(self, testdata_dir: Path):
        ta = TypeAdapter(PKLPath)
        p = testdata_dir / "sample.csv"
        with pytest.raises(ValidationError):
            ta.validate_python(str(p))


class TestHDF5Path:
    def test_positive(self, testdata_dir: Path):
        ta = TypeAdapter(HDF5Path)
        p = testdata_dir / "sample.h5"
        out = ta.validate_python(str(p))
        assert isinstance(out, Path)

    def test_negative(self, testdata_dir: Path):
        ta = TypeAdapter(HDF5Path)
        p = testdata_dir / "sample.csv"
        with pytest.raises(ValidationError):
            ta.validate_python(str(p))


class TestLogPath:
    def test_positive(self, testdata_dir: Path):
        ta = TypeAdapter(LogPath)
        p = testdata_dir / "sample.log"
        out = ta.validate_python(str(p))
        assert isinstance(out, Path)

    def test_negative(self, testdata_dir: Path):
        ta = TypeAdapter(LogPath)
        p = testdata_dir / "sample.csv"
        with pytest.raises(ValidationError):
            ta.validate_python(str(p))
