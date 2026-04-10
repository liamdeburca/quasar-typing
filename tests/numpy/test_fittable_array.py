"""Unit tests for FittableArray_ type aliases (finite + non-empty checks)."""

import pytest
import numpy as np

from quasar_typing.numpy import (
    FittableFloatArray, FittableFloatVector, FittableFloatMatrix, FittableFloatCube,
)


class TestFittableFloatArray:
    """Test FittableArray_ validation for floating point arrays."""
    
    def test_valid_fittable_array(self):
        """Valid fittable array with finite values should pass validation."""
        arr = np.array([1.0, 2.0, 3.0])
        result = FittableFloatArray._validate(arr)
        assert isinstance(result, np.ndarray)
        np.testing.assert_array_equal(result, arr)
    
    def test_valid_fittable_array_2d(self):
        """Valid 2D fittable array should pass validation."""
        arr = np.array([[1.0, 2.0], [3.0, 4.0]])
        result = FittableFloatArray._validate(arr)
        assert result.ndim == 2
    
    def test_valid_fittable_array_3d(self):
        """Valid 3D fittable array should pass validation."""
        arr = np.array([[[1.0, 2.0, 3.0]]])
        result = FittableFloatArray._validate(arr)
        assert result.ndim == 3
    
    def test_valid_negative_values(self):
        """Negative values should pass as long as they're finite."""
        arr = np.array([-1.0, -2.0, -3.0])
        result = FittableFloatArray._validate(arr)
        assert isinstance(result, np.ndarray)
    
    def test_valid_zero_values(self):
        """Zero values should pass."""
        arr = np.array([0.0, 0.0, 0.0])
        result = FittableFloatArray._validate(arr)
        np.testing.assert_array_equal(result, arr)
    
    def test_valid_very_large_finite_values(self):
        """Very large but finite values should pass."""
        arr = np.array([1e100, 1e200, 1e300])
        result = FittableFloatArray._validate(arr)
        assert isinstance(result, np.ndarray)
    
    def test_valid_very_small_finite_values(self):
        """Very small but finite values should pass."""
        arr = np.array([1e-100, 1e-200, 1e-300])
        result = FittableFloatArray._validate(arr)
        assert isinstance(result, np.ndarray)
    
    def test_invalid_non_array_input(self):
        """Non-array input should raise error."""
        with pytest.raises(Exception) as exc_info:
            FittableFloatArray._validate([1.0, 2.0, 3.0])
        assert 'Expected numpy array' in str(exc_info.value)
    
    def test_invalid_empty_array(self):
        """Empty array should raise error."""
        arr = np.array([])
        with pytest.raises(Exception) as exc_info:
            FittableFloatArray._validate(arr)
        assert 'Expected numpy array with at least one element' in str(exc_info.value)
    
    def test_invalid_empty_2d_array(self):
        """Empty 2D array should raise error."""
        arr = np.empty((0, 5))
        with pytest.raises(Exception) as exc_info:
            FittableFloatArray._validate(arr)
        assert 'Expected numpy array with at least one element' in str(exc_info.value)
    
    def test_invalid_empty_3d_array(self):
        """Empty 3D array should raise error."""
        arr = np.empty((0, 2, 3))
        with pytest.raises(Exception) as exc_info:
            FittableFloatArray._validate(arr)
        assert 'Expected numpy array with at least one element' in str(exc_info.value)
    
    def test_invalid_array_with_single_nan(self):
        """Array with single NaN value should raise error."""
        arr = np.array([1.0, np.nan, 3.0])
        with pytest.raises(Exception) as exc_info:
            FittableFloatArray._validate(arr)
        assert 'Expected numpy array with finite values' in str(exc_info.value)
        assert '1 non-finite' in str(exc_info.value)
    
    def test_invalid_array_with_single_inf(self):
        """Array with single inf value should raise error."""
        arr = np.array([1.0, np.inf, 3.0])
        with pytest.raises(Exception) as exc_info:
            FittableFloatArray._validate(arr)
        assert 'Expected numpy array with finite values' in str(exc_info.value)
        assert '1 non-finite' in str(exc_info.value)
    
    def test_invalid_array_with_single_neg_inf(self):
        """Array with single negative inf value should raise error."""
        arr = np.array([1.0, -np.inf, 3.0])
        with pytest.raises(Exception) as exc_info:
            FittableFloatArray._validate(arr)
        assert 'Expected numpy array with finite values' in str(exc_info.value)
        assert '1 non-finite' in str(exc_info.value)
    
    def test_invalid_array_with_multiple_nans(self):
        """Array with multiple NaN values should report count."""
        arr = np.array([np.nan, 2.0, np.nan, 4.0])
        with pytest.raises(Exception) as exc_info:
            FittableFloatArray._validate(arr)
        error_msg = str(exc_info.value)
        assert 'Expected numpy array with finite values' in error_msg
        assert '2 non-finite' in error_msg
    
    def test_invalid_array_with_multiple_non_finite_types(self):
        """Array with mixed non-finite values should report total count."""
        arr = np.array([1.0, np.nan, np.inf, -np.inf, 5.0])
        with pytest.raises(Exception) as exc_info:
            FittableFloatArray._validate(arr)
        error_msg = str(exc_info.value)
        assert 'Expected numpy array with finite values' in error_msg
        assert '3 non-finite' in error_msg
    
    def test_invalid_all_nan_array(self):
        """Array with all NaN values should raise error."""
        arr = np.array([np.nan, np.nan, np.nan])
        with pytest.raises(Exception) as exc_info:
            FittableFloatArray._validate(arr)
        error_msg = str(exc_info.value)
        assert 'Expected numpy array with finite values' in error_msg
        assert '3 non-finite' in error_msg
    
    def test_invalid_2d_array_with_nan(self):
        """2D array with any NaN should fail."""
        arr = np.array([[1.0, 2.0], [np.nan, 4.0]])
        with pytest.raises(Exception) as exc_info:
            FittableFloatArray._validate(arr)
        assert 'Expected numpy array with finite values' in str(exc_info.value)
    
    def test_invalid_integer_array(self):
        """Integer array should fail dtype check."""
        arr = np.array([1, 2, 3])
        with pytest.raises(Exception) as exc_info:
            FittableFloatArray._validate(arr)
        assert 'Expected numpy array of dtype' in str(exc_info.value)
    
    def test_validation_order_empty_before_finite(self):
        """Empty check should happen before finite check."""
        # Empty array should fail with 'at least one element' error, not finite error
        arr = np.array([])
        with pytest.raises(Exception) as exc_info:
            FittableFloatArray._validate(arr)
        assert 'at least one element' in str(exc_info.value)


class TestFittableFloatVector:
    """Test FittableArray_ validation for 1D floating point arrays."""
    
    def test_valid_fittable_vector(self):
        """Valid fittable 1D array should pass validation."""
        arr = np.array([1.0, 2.0, 3.0])
        result = FittableFloatVector._validate(arr)
        assert result.ndim == 1
        assert result.size == 3
    
    def test_valid_single_element_vector(self):
        """Single element vector should pass."""
        arr = np.array([42.0])
        result = FittableFloatVector._validate(arr)
        assert result.ndim == 1
        assert result.size == 1
    
    def test_invalid_empty_vector(self):
        """Empty vector should raise error."""
        arr = np.array([])
        with pytest.raises(Exception) as exc_info:
            FittableFloatVector._validate(arr)
        assert 'Expected numpy array with at least one element' in str(exc_info.value)
    
    def test_invalid_vector_with_nan(self):
        """Vector with NaN should raise error."""
        arr = np.array([1.0, np.nan, 3.0])
        with pytest.raises(Exception) as exc_info:
            FittableFloatVector._validate(arr)
        assert 'Expected numpy array with finite values' in str(exc_info.value)
    
    def test_invalid_vector_with_inf(self):
        """Vector with inf should raise error."""
        arr = np.array([1.0, np.inf, 3.0])
        with pytest.raises(Exception) as exc_info:
            FittableFloatVector._validate(arr)
        assert 'Expected numpy array with finite values' in str(exc_info.value)
    
    def test_invalid_2d_array(self):
        """2D array should fail ndim check."""
        arr = np.array([[1.0, 2.0], [3.0, 4.0]])
        with pytest.raises(Exception) as exc_info:
            FittableFloatVector._validate(arr)
        assert 'Expected numpy array of ndim 1' in str(exc_info.value)
    
    def test_invalid_3d_array(self):
        """3D array should fail ndim check."""
        arr = np.array([[[1.0, 2.0]]])
        with pytest.raises(Exception) as exc_info:
            FittableFloatVector._validate(arr)
        assert 'Expected numpy array of ndim 1' in str(exc_info.value)


class TestFittableFloatMatrix:
    """Test FittableArray_ validation for 2D floating point arrays."""
    
    def test_valid_fittable_matrix(self):
        """Valid fittable 2D array should pass validation."""
        arr = np.array([[1.0, 2.0], [3.0, 4.0]])
        result = FittableFloatMatrix._validate(arr)
        assert result.ndim == 2
    
    def test_valid_rectangular_matrix(self):
        """Rectangular matrix should pass."""
        arr = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        result = FittableFloatMatrix._validate(arr)
        assert result.shape == (2, 3)
    
    def test_invalid_empty_matrix(self):
        """Empty matrix should raise error."""
        arr = np.empty((0, 5))
        with pytest.raises(Exception) as exc_info:
            FittableFloatMatrix._validate(arr)
        assert 'Expected numpy array with at least one element' in str(exc_info.value)
    
    def test_invalid_matrix_with_nan(self):
        """Matrix with NaN should raise error."""
        arr = np.array([[1.0, np.nan], [3.0, 4.0]])
        with pytest.raises(Exception) as exc_info:
            FittableFloatMatrix._validate(arr)
        assert 'Expected numpy array with finite values' in str(exc_info.value)
    
    def test_invalid_1d_array(self):
        """1D array should fail ndim check."""
        arr = np.array([1.0, 2.0, 3.0])
        with pytest.raises(Exception) as exc_info:
            FittableFloatMatrix._validate(arr)
        assert 'Expected numpy array of ndim 2' in str(exc_info.value)
    
    def test_invalid_3d_array(self):
        """3D array should fail ndim check."""
        arr = np.ones((2, 2, 2), dtype=float)
        with pytest.raises(Exception) as exc_info:
            FittableFloatMatrix._validate(arr)
        assert 'Expected numpy array of ndim 2' in str(exc_info.value)


class TestFittableFloatCube:
    """Test FittableArray_ validation for 3D floating point arrays."""
    
    def test_valid_fittable_cube(self):
        """Valid fittable 3D array should pass validation."""
        arr = np.array([[[1.0, 2.0]]])
        result = FittableFloatCube._validate(arr)
        assert result.ndim == 3
    
    def test_valid_various_cube_shapes(self):
        """Various 3D shapes should pass."""
        for shape in [(2, 3, 4), (1, 1, 1), (5, 5, 5)]:
            arr = np.ones(shape, dtype=float)
            result = FittableFloatCube._validate(arr)
            assert result.shape == shape
    
    def test_invalid_empty_cube(self):
        """Empty cube should raise error."""
        arr = np.empty((0, 2, 2))
        with pytest.raises(Exception) as exc_info:
            FittableFloatCube._validate(arr)
        assert 'Expected numpy array with at least one element' in str(exc_info.value)
    
    def test_invalid_cube_with_inf(self):
        """Cube with inf should raise error."""
        arr = np.array([[[1.0, np.inf]]])
        with pytest.raises(Exception) as exc_info:
            FittableFloatCube._validate(arr)
        assert 'Expected numpy array with finite values' in str(exc_info.value)
    
    def test_invalid_2d_array(self):
        """2D array should fail ndim check."""
        arr = np.array([[1.0, 2.0], [3.0, 4.0]])
        with pytest.raises(Exception) as exc_info:
            FittableFloatCube._validate(arr)
        assert 'Expected numpy array of ndim 3' in str(exc_info.value)
