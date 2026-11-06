from pathlib import Path

import pytest
from pydantic import BaseModel, TypeAdapter, ValidationError

from quasar_typing.pathlib import (
    AnyDirPath,
    AnyFilePath,
    AnyHDF5Path,
    AnyJSONLikePath,
    AnyPath,
    AnyYAMLPath,
    ASCIIPath,
    CSVPath,
    DirPath,
    ExistingPath,
    FilePath,
    FITSPath,
    HDF5Path,
    JSONLikePath,
    JSONPath,
    LogPath,
    NewHDF5Path,
    NewJSONLikePath,
    NewPath,
    NewYAMLPath,
    PKLPath,
    TOMLPath,
    TOONPath,
    YAMLPath,
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


class TestYAMLVariants:
    """Test YAML path type variants (.yaml and .yml)."""

    def test_yaml_accepts_dot_yaml(self, testdata_dir: Path):
        """YAMLPath accepts .yaml extension."""
        ta = TypeAdapter(YAMLPath)
        p = testdata_dir / "sample.yaml"
        out = ta.validate_python(str(p))
        assert isinstance(out, Path)
        assert out.suffix == ".yaml"

    def test_yaml_accepts_dot_yml(self, testdata_dir: Path):
        """YAMLPath accepts .yml extension."""
        ta = TypeAdapter(YAMLPath)
        p = testdata_dir / "sample.yml"
        out = ta.validate_python(str(p))
        assert isinstance(out, Path)
        assert out.suffix == ".yml"

    def test_yaml_rejects_other_extensions(self, testdata_dir: Path):
        """YAMLPath rejects other extensions."""
        ta = TypeAdapter(YAMLPath)
        for invalid_file in ["sample.json", "sample.csv", "sample.toml"]:
            p = testdata_dir / invalid_file
            with pytest.raises(ValidationError):
                ta.validate_python(str(p))

    def test_any_yaml_path_accepts_both_extensions(self, testdata_dir: Path):
        """AnyYAMLPath accepts both .yaml and .yml."""
        ta = TypeAdapter(AnyYAMLPath)
        
        # .yaml
        p_yaml = testdata_dir / "sample.yaml"
        out_yaml = ta.validate_python(str(p_yaml))
        assert isinstance(out_yaml, Path)
        
        # .yml
        p_yml = testdata_dir / "sample.yml"
        out_yml = ta.validate_python(str(p_yml))
        assert isinstance(out_yml, Path)

    def test_new_yaml_path_rejects_existing_files(self, testdata_dir: Path):
        """NewYAMLPath rejects existing YAML files."""
        ta = TypeAdapter(NewYAMLPath)
        
        # Existing .yaml file should fail
        p = testdata_dir / "sample.yaml"
        with pytest.raises(ValidationError):
            ta.validate_python(str(p))

    def test_new_yaml_path_accepts_new_files(self, testdata_dir: Path):
        """NewYAMLPath accepts new YAML paths."""
        ta = TypeAdapter(NewYAMLPath)
        
        # Non-existent .yaml path should pass
        p = testdata_dir / "new_config.yaml"
        out = ta.validate_python(str(p))
        assert isinstance(out, Path)
        assert out.suffix == ".yaml"

    def test_yaml_in_model(self, testdata_dir: Path):
        """YAMLPath works in Pydantic model."""
        class Config(BaseModel):
            config_file: YAMLPath

        p = testdata_dir / "sample.yaml"
        config = Config(config_file=str(p))
        assert isinstance(config.config_file, Path)


class TestHDF5Variants:
    """Test HDF5 path type variants (.h5 and .hdf5)."""

    def test_hdf5_accepts_dot_h5(self, testdata_dir: Path):
        """HDF5Path accepts .h5 extension."""
        ta = TypeAdapter(HDF5Path)
        p = testdata_dir / "sample.h5"
        out = ta.validate_python(str(p))
        assert isinstance(out, Path)
        assert out.suffix == ".h5"

    def test_hdf5_accepts_dot_hdf5(self, testdata_dir: Path):
        """HDF5Path accepts .hdf5 extension."""
        ta = TypeAdapter(HDF5Path)
        p = testdata_dir / "sample.hdf5"
        out = ta.validate_python(str(p))
        assert isinstance(out, Path)
        assert out.suffix == ".hdf5"

    def test_hdf5_rejects_other_extensions(self, testdata_dir: Path):
        """HDF5Path rejects other extensions."""
        ta = TypeAdapter(HDF5Path)
        for invalid_file in ["sample.h4", "sample.json", "sample.csv"]:
            p = testdata_dir / invalid_file
            with pytest.raises(ValidationError):
                ta.validate_python(str(p))

    def test_any_hdf5_path_accepts_both_extensions(self, testdata_dir: Path):
        """AnyHDF5Path accepts both .h5 and .hdf5."""
        ta = TypeAdapter(AnyHDF5Path)
        
        # .h5
        p_h5 = testdata_dir / "sample.h5"
        out_h5 = ta.validate_python(str(p_h5))
        assert isinstance(out_h5, Path)
        
        # .hdf5
        p_hdf5 = testdata_dir / "sample.hdf5"
        out_hdf5 = ta.validate_python(str(p_hdf5))
        assert isinstance(out_hdf5, Path)

    def test_new_hdf5_path_rejects_existing_files(self, testdata_dir: Path):
        """NewHDF5Path rejects existing HDF5 files."""
        ta = TypeAdapter(NewHDF5Path)
        
        # Existing .h5 file should fail
        p = testdata_dir / "sample.h5"
        with pytest.raises(ValidationError):
            ta.validate_python(str(p))

    def test_new_hdf5_path_accepts_new_files(self, testdata_dir: Path):
        """NewHDF5Path accepts new HDF5 paths."""
        ta = TypeAdapter(NewHDF5Path)
        
        # Non-existent .h5 path should pass
        p = testdata_dir / "new_data.h5"
        out = ta.validate_python(str(p))
        assert isinstance(out, Path)
        assert out.suffix == ".h5"

    def test_hdf5_in_model(self, testdata_dir: Path):
        """HDF5Path works in Pydantic model."""
        class DataModel(BaseModel):
            data_file: HDF5Path

        p = testdata_dir / "sample.h5"
        model = DataModel(data_file=str(p))
        assert isinstance(model.data_file, Path)


class TestJSONLikePath:
    """Test JSONLikePath union types (JSON|YAML|TOML|TOON)."""

    def test_json_like_accepts_json(self, testdata_dir: Path):
        """JSONLikePath accepts JSON files."""
        ta = TypeAdapter(JSONLikePath)
        p = testdata_dir / "sample.json"
        out = ta.validate_python(str(p))
        assert isinstance(out, Path)
        assert out.suffix == ".json"

    def test_json_like_accepts_yaml_variants(self, testdata_dir: Path):
        """JSONLikePath accepts YAML files (.yaml and .yml)."""
        ta = TypeAdapter(JSONLikePath)
        
        for yaml_file in ["sample.yaml", "sample.yml"]:
            p = testdata_dir / yaml_file
            out = ta.validate_python(str(p))
            assert isinstance(out, Path)
            assert out.suffix in {".yaml", ".yml"}

    def test_json_like_accepts_toml(self, testdata_dir: Path):
        """JSONLikePath accepts TOML files."""
        ta = TypeAdapter(JSONLikePath)
        p = testdata_dir / "sample.toml"
        out = ta.validate_python(str(p))
        assert isinstance(out, Path)
        assert out.suffix == ".toml"

    def test_json_like_accepts_toon(self, testdata_dir: Path):
        """JSONLikePath accepts TOON files."""
        ta = TypeAdapter(JSONLikePath)
        p = testdata_dir / "sample.toon"
        out = ta.validate_python(str(p))
        assert isinstance(out, Path)
        assert out.suffix == ".toon"

    def test_json_like_rejects_non_json_like(self, testdata_dir: Path):
        """JSONLikePath rejects non-JSON-like files."""
        ta = TypeAdapter(JSONLikePath)
        
        for invalid_file in ["sample.csv", "sample.fits", "sample.log"]:
            p = testdata_dir / invalid_file
            with pytest.raises(ValidationError):
                ta.validate_python(str(p))

    def test_any_json_like_path_accepts_all_formats(
        self, testdata_dir: Path
    ):
        """AnyJSONLikePath accepts all JSON-like formats."""
        ta = TypeAdapter(AnyJSONLikePath)
        
        json_like_files = [
            "sample.json",
            "sample.yaml",
            "sample.yml",
            "sample.toml",
            "sample.toon",
        ]
        
        for filename in json_like_files:
            p = testdata_dir / filename
            out = ta.validate_python(str(p))
            assert isinstance(out, Path)

    def test_new_json_like_path_accepts_new_files(
        self, testdata_dir: Path
    ):
        """NewJSONLikePath accepts new JSON-like paths."""
        ta = TypeAdapter(NewJSONLikePath)
        
        # New YAML file path
        p_yaml = testdata_dir / "config.yaml"
        out_yaml = ta.validate_python(str(p_yaml))
        assert isinstance(out_yaml, Path)
        
        # New JSON file path
        p_json = testdata_dir / "data.json"
        out_json = ta.validate_python(str(p_json))
        assert isinstance(out_json, Path)

    def test_json_like_rejects_new_non_json_like_path(
        self, testdata_dir: Path
    ):
        """NewJSONLikePath rejects new non-JSON-like paths."""
        ta = TypeAdapter(NewJSONLikePath)
        
        # Non-JSON-like extension
        p = testdata_dir / "data.csv"
        with pytest.raises(ValidationError):
            ta.validate_python(str(p))

    def test_json_like_in_config_model(self, testdata_dir: Path):
        """JSONLikePath works in realistic config model."""
        class AppConfig(BaseModel):
            config_file: JSONLikePath
            data_file: JSONLikePath

        config = AppConfig(
            config_file=str(testdata_dir / "sample.yaml"),
            data_file=str(testdata_dir / "sample.json"),
        )
        
        assert config.config_file.suffix == ".yaml"
        assert config.data_file.suffix == ".json"

    def test_any_json_like_path_hierarchy(self, testdata_dir: Path):
        """AnyJSONLikePath includes all specifics (JSON,YAML,TOML,TOON)."""
        ta_any = TypeAdapter(AnyJSONLikePath)
        ta_json = TypeAdapter(JSONLikePath)
        
        # Both should accept the same JSON-like formats
        test_file = testdata_dir / "sample.yaml"
        
        # AnyJSONLikePath should accept existing
        out_any = ta_any.validate_python(str(test_file))
        assert isinstance(out_any, Path)
        
        # JSONLikePath should also accept existing
        out_existing = ta_json.validate_python(str(test_file))
        assert isinstance(out_existing, Path)
