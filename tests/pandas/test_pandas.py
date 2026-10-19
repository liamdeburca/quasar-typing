"""Test pandas type validation using pydantic TypeAdapter."""

import numpy as np
import pandas as pd
import pytest
from pydantic import TypeAdapter, ValidationError

from quasar_typing.pandas import DataFrameType, StrictDataFrameType


class TestStrictDataFrameTypeValid:
    """Tests for valid StrictDataFrameType inputs (isinstance validation only)."""

    def test_simple_dataframe_valid(self, simple_dataframe):
        """Simple DataFrame should pass validation."""
        adapter = TypeAdapter(StrictDataFrameType)
        result = adapter.validate_python(simple_dataframe)
        assert isinstance(result, pd.DataFrame)

    def test_empty_dataframe_valid(self, empty_dataframe):
        """Empty DataFrame should pass validation."""
        adapter = TypeAdapter(StrictDataFrameType)
        result = adapter.validate_python(empty_dataframe)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_numeric_dataframe_valid(self, numeric_dataframe):
        """Numeric DataFrame should pass validation."""
        adapter = TypeAdapter(StrictDataFrameType)
        result = adapter.validate_python(numeric_dataframe)
        assert isinstance(result, pd.DataFrame)
        assert result.shape == (5, 3)

    def test_multiindex_dataframe_valid(self, multiindex_dataframe):
        """DataFrame with MultiIndex should pass validation."""
        adapter = TypeAdapter(StrictDataFrameType)
        result = adapter.validate_python(multiindex_dataframe)
        assert isinstance(result, pd.DataFrame)
        assert isinstance(result.index, pd.MultiIndex)

    def test_strict_maintains_identity(self, simple_dataframe):
        """Validated DataFrame should be the same object."""
        adapter = TypeAdapter(StrictDataFrameType)
        result = adapter.validate_python(simple_dataframe)
        assert result is simple_dataframe

    def test_strict_maintains_data(self, simple_dataframe):
        """Validated DataFrame should maintain all data."""
        adapter = TypeAdapter(StrictDataFrameType)
        result = adapter.validate_python(simple_dataframe)
        pd.testing.assert_frame_equal(result, simple_dataframe)


class TestStrictDataFrameTypeInvalid:
    """Tests for invalid StrictDataFrameType inputs."""

    def test_strict_rejects_none(self):
        """None should raise validation error."""
        adapter = TypeAdapter(StrictDataFrameType)
        with pytest.raises(ValidationError):
            adapter.validate_python(None)

    def test_strict_rejects_dict(self, dict_for_dataframe):
        """Plain dict should raise validation error (no coercion in strict mode)."""
        adapter = TypeAdapter(StrictDataFrameType)
        with pytest.raises(ValidationError):
            adapter.validate_python(dict_for_dataframe)

    def test_strict_rejects_list(self, list_of_lists_for_dataframe):
        """List should raise validation error (no coercion in strict mode)."""
        adapter = TypeAdapter(StrictDataFrameType)
        with pytest.raises(ValidationError):
            adapter.validate_python(list_of_lists_for_dataframe)

    def test_strict_rejects_series(self):
        """Series should raise validation error."""
        adapter = TypeAdapter(StrictDataFrameType)
        series = pd.Series([1, 2, 3])
        with pytest.raises(ValidationError):
            adapter.validate_python(series)

    def test_strict_rejects_string(self):
        """String should raise validation error."""
        adapter = TypeAdapter(StrictDataFrameType)
        with pytest.raises(ValidationError):
            adapter.validate_python("not a dataframe")

    def test_strict_rejects_integer(self):
        """Integer should raise validation error."""
        adapter = TypeAdapter(StrictDataFrameType)
        with pytest.raises(ValidationError):
            adapter.validate_python(42)

    def test_strict_rejects_array(self):
        """NumPy array should raise validation error."""
        adapter = TypeAdapter(StrictDataFrameType)
        array = np.array([[1, 2], [3, 4]])
        with pytest.raises(ValidationError):
            adapter.validate_python(array)


class TestDataFrameTypeValid:
    """Tests for valid DataFrameType inputs (with coercion)."""

    def test_dataframe_valid(self, simple_dataframe):
        """DataFrame should pass validation."""
        adapter = TypeAdapter(DataFrameType.__value__)
        result = adapter.validate_python(simple_dataframe)
        assert isinstance(result, pd.DataFrame)
        pd.testing.assert_frame_equal(result, simple_dataframe)

    def test_dict_coerced_to_dataframe(self, dict_for_dataframe):
        """Dict should be coerced to DataFrame."""
        adapter = TypeAdapter(DataFrameType.__value__)
        result = adapter.validate_python(dict_for_dataframe)
        assert isinstance(result, pd.DataFrame)
        assert list(result.columns) == ['A', 'B']
        assert len(result) == 3

    def test_dict_of_series_coerced(self, dict_of_series_for_dataframe):
        """Dictionary of Series should be coerced to DataFrame."""
        adapter = TypeAdapter(DataFrameType.__value__)
        result = adapter.validate_python(dict_of_series_for_dataframe)
        assert isinstance(result, pd.DataFrame)
        assert list(result.columns) == ['A', 'B']

    def test_list_coerced_to_dataframe(self, list_of_lists_for_dataframe):
        """List of lists should be coerced to DataFrame."""
        adapter = TypeAdapter(DataFrameType.__value__)
        result = adapter.validate_python(list_of_lists_for_dataframe)
        assert isinstance(result, pd.DataFrame)
        assert result.shape == (3, 3)

    def test_array_coerced_to_dataframe(self):
        """NumPy array should be coerced to DataFrame."""
        adapter = TypeAdapter(DataFrameType.__value__)
        array = np.array([[1, 2, 3], [4, 5, 6]])
        result = adapter.validate_python(array)
        assert isinstance(result, pd.DataFrame)
        assert result.shape == (2, 3)

    def test_dataframe_coercion_maintains_structure(self, simple_dataframe):
        """DataFrame coercion should maintain structure."""
        adapter = TypeAdapter(DataFrameType.__value__)
        result = adapter.validate_python(simple_dataframe)
        # After coercion, should still be the same
        pd.testing.assert_frame_equal(result, simple_dataframe)


class TestDataFrameTypeInvalid:
    """Tests for invalid DataFrameType inputs (even with coercion)."""

    def test_dataframe_rejects_none_creates_empty(self):
        """None is coerced to an empty DataFrame (not an error)."""
        adapter = TypeAdapter(DataFrameType.__value__)
        result = adapter.validate_python(None)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_dataframe_rejects_string(self):
        """String should raise validation error (can't coerce meaningfully)."""
        adapter = TypeAdapter(DataFrameType.__value__)
        # Note: pd.DataFrame(string) might create a DataFrame with 1 column,
        # but we expect it to fail validation
        with pytest.raises(ValidationError):
            adapter.validate_python("not a dataframe")

    def test_dataframe_rejects_integer(self):
        """Integer should raise validation error."""
        adapter = TypeAdapter(DataFrameType.__value__)
        with pytest.raises(ValidationError):
            adapter.validate_python(42)

    def test_dataframe_series_coerced_to_dataframe(self):
        """Series is coerced to a DataFrame with one column (not an error)."""
        adapter = TypeAdapter(DataFrameType.__value__)
        series = pd.Series([1, 2, 3])
        result = adapter.validate_python(series)
        assert isinstance(result, pd.DataFrame)
        assert result.shape == (3, 1)


class TestDataFrameComparison:
    """Tests comparing StrictDataFrameType and DataFrameType behavior."""

    def test_strict_vs_coerce_with_dict(self, dict_for_dataframe):
        """StrictDataFrameType rejects dict, but DataFrameType accepts it."""
        strict_adapter = TypeAdapter(StrictDataFrameType)
        coerce_adapter = TypeAdapter(DataFrameType.__value__)
        
        # Strict rejects
        with pytest.raises(ValidationError):
            strict_adapter.validate_python(dict_for_dataframe)
        
        # Coerce accepts and converts
        result = coerce_adapter.validate_python(dict_for_dataframe)
        assert isinstance(result, pd.DataFrame)

    def test_strict_vs_coerce_with_list(self, list_of_lists_for_dataframe):
        """StrictDataFrameType rejects list, but DataFrameType accepts it."""
        strict_adapter = TypeAdapter(StrictDataFrameType)
        coerce_adapter = TypeAdapter(DataFrameType.__value__)
        
        # Strict rejects
        with pytest.raises(ValidationError):
            strict_adapter.validate_python(list_of_lists_for_dataframe)
        
        # Coerce accepts and converts
        result = coerce_adapter.validate_python(list_of_lists_for_dataframe)
        assert isinstance(result, pd.DataFrame)

    def test_both_accept_dataframe(self, simple_dataframe):
        """Both StrictDataFrameType and DataFrameType accept actual DataFrames."""
        strict_adapter = TypeAdapter(StrictDataFrameType)
        coerce_adapter = TypeAdapter(DataFrameType.__value__)
        
        strict_result = strict_adapter.validate_python(simple_dataframe)
        coerce_result = coerce_adapter.validate_python(simple_dataframe)
        
        assert isinstance(strict_result, pd.DataFrame)
        assert isinstance(coerce_result, pd.DataFrame)
        pd.testing.assert_frame_equal(strict_result, coerce_result)


class TestEdgeCases:
    """Tests for edge cases and special DataFrames."""

    def test_dataframe_with_nan_values(self):
        """DataFrame with NaN values should pass validation."""
        df = pd.DataFrame({
            'A': [1.0, np.nan, 3.0],
            'B': [np.nan, 5.0, np.nan]
        })
        adapter = TypeAdapter(StrictDataFrameType)
        result = adapter.validate_python(df)
        assert isinstance(result, pd.DataFrame)
        assert result.isna().sum().sum() == 3

    def test_dataframe_with_mixed_types(self):
        """DataFrame with mixed column types should pass validation."""
        df = pd.DataFrame({
            'int_col': [1, 2, 3],
            'float_col': [1.5, 2.5, 3.5],
            'str_col': ['a', 'b', 'c'],
            'bool_col': [True, False, True]
        })
        adapter = TypeAdapter(StrictDataFrameType)
        result = adapter.validate_python(df)
        assert isinstance(result, pd.DataFrame)
        assert len(result.columns) == 4

    def test_large_dataframe(self):
        """Large DataFrame should pass validation."""
        df = pd.DataFrame({
            'A': np.arange(10000),
            'B': np.random.random(10000)
        })
        adapter = TypeAdapter(StrictDataFrameType)
        result = adapter.validate_python(df)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 10000
