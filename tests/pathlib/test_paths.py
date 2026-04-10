import pytest
from pathlib import Path
from pydantic import BaseModel, ValidationError
from quasar_typing.pathlib import (
    # Absolute Paths
    AnyAbsolutePath,
    NewAbsolutePath,
    AbsolutePath,
    # Absolute File Paths
    AnyAbsoluteFilePath,
    NewAbsoluteFilePath,
    AbsoluteFilePath,
    # Absolute Directory Paths
    AnyAbsoluteDirPath,
    NewAbsoluteDirPath,
    AbsoluteDirPath,
    # File Format Paths
    AnyAbsoluteCSVPath,
    NewAbsoluteCSVPath,
    AbsoluteCSVPath,
    AnyAbsoluteASCIIPath,
    NewAbsoluteASCIIPath,
    AbsoluteASCIIPath,
    AnyAbsoluteFITSPath,
    NewAbsoluteFITSPath,
    AbsoluteFITSPath,
    AnyAbsoluteJSONPath,
    NewAbsoluteJSONPath,
    AbsoluteJSONPath,
    AnyAbsolutePKLPath,
    NewAbsolutePKLPath,
    AbsolutePKLPath,
)

# Setup test paths
TEST_DIR = Path(__file__).parent / "test_paths"
EXISTING_FILE = TEST_DIR / "test_file.txt"
EXISTING_DIR = TEST_DIR / "existing_dir"
EXISTING_CSV = TEST_DIR / "data.csv"
EXISTING_ASCII = TEST_DIR / "data.asc"
EXISTING_FITS = TEST_DIR / "data.fits"
EXISTING_JSON = TEST_DIR / "config.json"
EXISTING_PKL = TEST_DIR / "data.pkl"
NON_EXISTENT_FILE = TEST_DIR / "nonexistent_file.txt"
NON_EXISTENT_CSV = TEST_DIR / "nonexistent.csv"


class TestAbsolutePaths:
    """Test absolute path validation"""

    def test_any_absolute_path_with_existing_file(self):
        class Model(BaseModel):
            path: AnyAbsolutePath

        m = Model(path=str(EXISTING_FILE))
        assert isinstance(m.path, Path)

    def test_any_absolute_path_with_non_existent_path(self):
        class Model(BaseModel):
            path: AnyAbsolutePath

        m = Model(path=str(NON_EXISTENT_FILE))
        assert isinstance(m.path, Path)

    def test_absolute_path_with_relative_path_fails(self):
        class Model(BaseModel):
            path: AnyAbsolutePath

        with pytest.raises(ValidationError):
            Model(path="relative/path.txt")

    def test_new_absolute_path_with_existing_file_fails(self):
        class Model(BaseModel):
            path: NewAbsolutePath

        with pytest.raises(ValidationError):
            Model(path=str(EXISTING_FILE))

    def test_new_absolute_path_with_non_existent_file(self):
        class Model(BaseModel):
            path: NewAbsolutePath

        m = Model(path=str(NON_EXISTENT_FILE))
        assert isinstance(m.path, Path)

    def test_absolute_path_with_existing_file(self):
        class Model(BaseModel):
            path: AbsolutePath

        m = Model(path=str(EXISTING_FILE))
        assert isinstance(m.path, Path)

    def test_absolute_path_with_non_existent_file_fails(self):
        class Model(BaseModel):
            path: AbsolutePath

        with pytest.raises(ValidationError):
            Model(path=str(NON_EXISTENT_FILE))


class TestAbsoluteFilePaths:
    """Test absolute file path validation"""

    def test_any_absolute_file_path(self):
        class Model(BaseModel):
            path: AnyAbsoluteFilePath

        m = Model(path=str(EXISTING_FILE))
        assert isinstance(m.path, Path)

    def test_any_absolute_file_path_with_directory_fails(self):
        class Model(BaseModel):
            path: AnyAbsoluteFilePath

        with pytest.raises(ValidationError):
            Model(path=str(EXISTING_DIR))

    def test_new_absolute_file_path(self):
        class Model(BaseModel):
            path: NewAbsoluteFilePath

        m = Model(path=str(NON_EXISTENT_FILE))
        assert isinstance(m.path, Path)

    def test_absolute_file_path_with_existing_file(self):
        class Model(BaseModel):
            path: AbsoluteFilePath

        m = Model(path=str(EXISTING_FILE))
        assert isinstance(m.path, Path)


class TestAbsoluteDirPaths:
    """Test absolute directory path validation"""

    def test_any_absolute_dir_path(self):
        class Model(BaseModel):
            path: AnyAbsoluteDirPath

        m = Model(path=str(EXISTING_DIR))
        assert isinstance(m.path, Path)

    def test_any_absolute_dir_path_with_file_fails(self):
        class Model(BaseModel):
            path: AnyAbsoluteDirPath

        with pytest.raises(ValidationError):
            Model(path=str(EXISTING_FILE))

    def test_new_absolute_dir_path(self):
        class Model(BaseModel):
            path: NewAbsoluteDirPath

        m = Model(path=str(TEST_DIR / "new_directory"))
        assert isinstance(m.path, Path)

    def test_absolute_dir_path_with_existing_directory(self):
        class Model(BaseModel):
            path: AbsoluteDirPath

        m = Model(path=str(EXISTING_DIR))
        assert isinstance(m.path, Path)


class TestCSVPaths:
    """Test CSV file path validation"""

    def test_any_absolute_csv_path(self):
        class Model(BaseModel):
            path: AnyAbsoluteCSVPath

        m = Model(path=str(EXISTING_CSV))
        assert isinstance(m.path, Path)

    def test_any_absolute_csv_path_with_wrong_extension_fails(self):
        class Model(BaseModel):
            path: AnyAbsoluteCSVPath

        with pytest.raises(ValidationError):
            Model(path=str(EXISTING_FILE))

    def test_absolute_csv_path_with_existing_file(self):
        class Model(BaseModel):
            path: AbsoluteCSVPath

        m = Model(path=str(EXISTING_CSV))
        assert isinstance(m.path, Path)


class TestASCIIPaths:
    """Test ASCII file path validation"""

    def test_any_absolute_ascii_path(self):
        class Model(BaseModel):
            path: AnyAbsoluteASCIIPath

        m = Model(path=str(EXISTING_ASCII))
        assert isinstance(m.path, Path)

    def test_absolute_ascii_path_with_existing_file(self):
        class Model(BaseModel):
            path: AbsoluteASCIIPath

        m = Model(path=str(EXISTING_ASCII))
        assert isinstance(m.path, Path)


class TestFITSPaths:
    """Test FITS file path validation"""

    def test_any_absolute_fits_path(self):
        class Model(BaseModel):
            path: AnyAbsoluteFITSPath

        m = Model(path=str(EXISTING_FITS))
        assert isinstance(m.path, Path)

    def test_absolute_fits_path_with_existing_file(self):
        class Model(BaseModel):
            path: AbsoluteFITSPath

        m = Model(path=str(EXISTING_FITS))
        assert isinstance(m.path, Path)


class TestJSONPaths:
    """Test JSON file path validation"""

    def test_any_absolute_json_path(self):
        class Model(BaseModel):
            path: AnyAbsoluteJSONPath

        m = Model(path=str(EXISTING_JSON))
        assert isinstance(m.path, Path)

    def test_absolute_json_path_with_existing_file(self):
        class Model(BaseModel):
            path: AbsoluteJSONPath

        m = Model(path=str(EXISTING_JSON))
        assert isinstance(m.path, Path)


class TestPKLPaths:
    """Test PKL file path validation"""

    def test_any_absolute_pkl_path(self):
        class Model(BaseModel):
            path: AnyAbsolutePKLPath

        m = Model(path=str(EXISTING_PKL))
        assert isinstance(m.path, Path)

    def test_absolute_pkl_path_with_existing_file(self):
        class Model(BaseModel):
            path: AbsolutePKLPath

        m = Model(path=str(EXISTING_PKL))
        assert isinstance(m.path, Path)


class TestPathConversions:
    """Test that string and Path objects are both accepted"""

    def test_string_path_input(self):
        class Model(BaseModel):
            path: AnyAbsolutePath

        m = Model(path=str(EXISTING_FILE))
        assert isinstance(m.path, Path)

    def test_path_object_input(self):
        class Model(BaseModel):
            path: AnyAbsolutePath

        m = Model(path=EXISTING_FILE)
        assert isinstance(m.path, Path)

    def test_invalid_input_type_fails(self):
        class Model(BaseModel):
            path: AnyAbsolutePath

        with pytest.raises(ValidationError):
            Model(path=123)
