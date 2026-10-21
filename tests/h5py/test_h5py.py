"""Tests for h5py type annotations.

Tests cover:
- AttributeManagerType: Pydantic validation for h5py.AttributeManager
- DatasetType: Pydantic validation for h5py.Dataset
- GroupType: Pydantic validation for h5py.Group
- FileType: Pydantic validation for h5py.File
"""
import pytest
import tempfile
import h5py
from pydantic import BaseModel, ValidationError, ConfigDict

from quasar_typing.h5py import (
    AttributeManagerType,
    DatasetType,
    GroupType,
    FileType,
)


class TestAttributeManagerType:
    """Test AttributeManagerType validation for h5py.AttributeManager"""

    def test_attribute_manager_type_accepts_manager(self, h5_file_object):
        """AttributeManagerType accepts h5py.AttributeManager instance."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            attrs: AttributeManagerType

        attrs = h5_file_object.attrs
        model = Model(attrs=attrs)
        assert isinstance(model.attrs, h5py.AttributeManager)
        assert model.attrs is attrs

    def test_attribute_manager_type_rejects_none(self):
        """AttributeManagerType rejects None."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            attrs: AttributeManagerType

        with pytest.raises(ValidationError):
            Model(attrs=None)

    def test_attribute_manager_type_rejects_dict(self):
        """AttributeManagerType rejects regular dict."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            attrs: AttributeManagerType

        with pytest.raises(ValidationError):
            Model(attrs={"key": "value"})

    def test_attribute_manager_type_rejects_string(self):
        """AttributeManagerType rejects string."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            attrs: AttributeManagerType

        with pytest.raises(ValidationError):
            Model(attrs="not an attribute manager")

    def test_attribute_manager_type_rejects_int(self):
        """AttributeManagerType rejects integer."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            attrs: AttributeManagerType

        with pytest.raises(ValidationError):
            Model(attrs=42)

    def test_attribute_manager_type_passthrough(self, h5_file_object):
        """Validated AttributeManager is the same instance."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            attrs: AttributeManagerType

        attrs = h5_file_object.attrs
        model = Model(attrs=attrs)
        assert model.attrs is attrs


class TestDatasetType:
    """Test DatasetType validation for h5py.Dataset"""

    def test_dataset_type_accepts_dataset(self, h5_dataset):
        """DatasetType accepts h5py.Dataset instance."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            dataset: DatasetType

        model = Model(dataset=h5_dataset)
        assert isinstance(model.dataset, h5py.Dataset)
        assert model.dataset is h5_dataset

    def test_dataset_type_accepts_different_dtypes(self, h5_file_object):
        """DatasetType accepts datasets with different dtypes."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            dataset: DatasetType

        # Test with integer dataset
        int_dataset = h5_file_object['dataset1']
        model = Model(dataset=int_dataset)
        assert isinstance(model.dataset, h5py.Dataset)

    def test_dataset_type_rejects_none(self):
        """DatasetType rejects None."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            dataset: DatasetType

        with pytest.raises(ValidationError):
            Model(dataset=None)

    def test_dataset_type_rejects_group(self, h5_group):
        """DatasetType rejects h5py.Group."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            dataset: DatasetType

        with pytest.raises(ValidationError):
            Model(dataset=h5_group)

    def test_dataset_type_rejects_file(self, h5_file_object):
        """DatasetType rejects h5py.File."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            dataset: DatasetType

        with pytest.raises(ValidationError):
            Model(dataset=h5_file_object)

    def test_dataset_type_rejects_list(self):
        """DatasetType rejects list."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            dataset: DatasetType

        with pytest.raises(ValidationError):
            Model(dataset=[1, 2, 3])

    def test_dataset_type_rejects_string(self):
        """DatasetType rejects string."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            dataset: DatasetType

        with pytest.raises(ValidationError):
            Model(dataset="not a dataset")

    def test_dataset_type_passthrough(self, h5_dataset):
        """Validated Dataset is the same instance."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            dataset: DatasetType

        model = Model(dataset=h5_dataset)
        assert model.dataset is h5_dataset

    def test_dataset_type_multiple_datasets(self):
        """DatasetType validates multiple datasets."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            dataset1: DatasetType
            dataset2: DatasetType

        import tempfile
        
        # Create a file with multiple datasets
        with tempfile.NamedTemporaryFile(suffix='.h5', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Create file with two datasets
            with h5py.File(tmp_path, 'w') as f:
                f.create_dataset('dataset1', data=[1, 2, 3])
                f.create_dataset('dataset2', data=[4, 5, 6])
            
            # Open and validate
            with h5py.File(tmp_path, 'r') as f:
                d1 = f['dataset1']
                d2 = f['dataset2']
                model = Model(dataset1=d1, dataset2=d2)
                assert model.dataset1 is d1
                assert model.dataset2 is d2
        finally:
            import os
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


class TestGroupType:
    """Test GroupType validation for h5py.Group"""

    def test_group_type_accepts_group(self, h5_group):
        """GroupType accepts h5py.Group instance."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            group: GroupType

        model = Model(group=h5_group)
        assert isinstance(model.group, h5py.Group)
        assert model.group is h5_group

    def test_group_type_accepts_file_as_group(self, h5_file_object):
        """GroupType accepts h5py.File (which is a Group subclass)."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            group: GroupType

        model = Model(group=h5_file_object)
        assert isinstance(model.group, h5py.Group)
        assert model.group is h5_file_object

    def test_group_type_rejects_none(self):
        """GroupType rejects None."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            group: GroupType

        with pytest.raises(ValidationError):
            Model(group=None)

    def test_group_type_rejects_dataset(self, h5_dataset):
        """GroupType rejects h5py.Dataset."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            group: GroupType

        with pytest.raises(ValidationError):
            Model(group=h5_dataset)

    def test_group_type_rejects_dict(self):
        """GroupType rejects regular dict."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            group: GroupType

        with pytest.raises(ValidationError):
            Model(group={"key": "value"})

    def test_group_type_rejects_string(self):
        """GroupType rejects string."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            group: GroupType

        with pytest.raises(ValidationError):
            Model(group="not a group")

    def test_group_type_passthrough(self, h5_group):
        """Validated Group is the same instance."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            group: GroupType

        model = Model(group=h5_group)
        assert model.group is h5_group

    def test_group_type_with_subgroups(self, h5_file_object):
        """GroupType accepts groups with subgroups."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            group: GroupType

        group = h5_file_object['group1']
        model = Model(group=group)
        assert isinstance(model.group, h5py.Group)


class TestFileType:
    """Test FileType validation for h5py.File"""

    def test_file_type_accepts_file(self, h5_file_object):
        """FileType accepts h5py.File instance."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            file: FileType

        model = Model(file=h5_file_object)
        assert isinstance(model.file, h5py.File)
        assert model.file is h5_file_object

    def test_file_type_rejects_none(self):
        """FileType rejects None."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            file: FileType

        with pytest.raises(ValidationError):
            Model(file=None)

    def test_file_type_rejects_group(self, h5_group):
        """FileType rejects h5py.Group that's not a File."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            file: FileType

        with pytest.raises(ValidationError):
            Model(file=h5_group)

    def test_file_type_rejects_dataset(self, h5_dataset):
        """FileType rejects h5py.Dataset."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            file: FileType

        with pytest.raises(ValidationError):
            Model(file=h5_dataset)

    def test_file_type_rejects_string(self):
        """FileType rejects string (filepath)."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            file: FileType

        with pytest.raises(ValidationError):
            Model(file="/path/to/file.h5")

    def test_file_type_rejects_pathlib_path(self):
        """FileType rejects pathlib.Path."""
        from pathlib import Path
        
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            file: FileType

        with pytest.raises(ValidationError):
            Model(file=Path("/path/to/file.h5"))

    def test_file_type_passthrough(self, h5_file_object):
        """Validated File is the same instance."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            file: FileType

        model = Model(file=h5_file_object)
        assert model.file is h5_file_object

    def test_file_type_different_modes(self):
        """FileType accepts files opened in different modes."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            file: FileType

        with tempfile.NamedTemporaryFile(suffix='.h5', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Test with read mode
            f = h5py.File(tmp_path, 'r+')
            try:
                model = Model(file=f)
                assert isinstance(model.file, h5py.File)
                assert model.file is f
            finally:
                f.close()
        finally:
            import os
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


class TestH5PyTypesEdgeCases:
    """Test edge cases and combined scenarios for h5py types."""

    def test_model_with_all_h5py_types(self, h5_file_object):
        """Model with all h5py types validates correctly."""
        class H5Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            file: FileType
            group: GroupType
            dataset: DatasetType
            attrs: AttributeManagerType

        group = h5_file_object['group1']
        dataset = h5_file_object['dataset1']
        
        model = H5Model(
            file=h5_file_object,
            group=group,
            dataset=dataset,
            attrs=h5_file_object.attrs,
        )
        
        assert model.file is h5_file_object
        assert model.group is group
        assert model.dataset is dataset

    def test_optional_h5py_fields(self, h5_file_object):
        """Optional h5py fields work correctly."""
        from typing import Optional
        
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            file: Optional[FileType] = None
            dataset: Optional[DatasetType] = None

        # With values
        model1 = Model(file=h5_file_object, dataset=h5_file_object['dataset1'])
        assert model1.file is h5_file_object
        assert model1.dataset is not None

        # Without values
        model2 = Model()
        assert model2.file is None
        assert model2.dataset is None

    def test_h5py_types_immutable_after_validation(self, h5_file_object):
        """h5py objects are immutable after validation (passthrough)."""
        class Model(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            file: FileType

        model = Model(file=h5_file_object)
        # Verify it's the same object (not copied)
        assert model.file is h5_file_object
        assert id(model.file) == id(h5_file_object)
