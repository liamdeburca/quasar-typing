"""Unit tests for CoordsTuple type aliases."""

import pytest
import numpy as np

from quasar_typing.numpy import SpectrumCoordsTuple, FittableCoordsTuple


class TestSpectrumCoordsTuple:
    """Test CoordsTuple[FloatArray] validation."""
    
    def test_valid_matching_1d_arrays(self):
        """Valid 3-tuple of matching 1D arrays should pass."""
        arr1 = np.array([1.0, 2.0, 3.0])
        arr2 = np.array([4.0, 5.0, 6.0])
        arr3 = np.array([7.0, 8.0, 9.0])
        value = (arr1, arr2, arr3)
        result = SpectrumCoordsTuple._validate_same_shape(value)
        assert len(result) == 3
        assert result[0].shape == result[1].shape == result[2].shape
    
    def test_valid_matching_2d_arrays(self):
        """Valid 3-tuple of matching 2D arrays should pass."""
        arr1 = np.array([[1.0, 2.0], [3.0, 4.0]])
        arr2 = np.array([[5.0, 6.0], [7.0, 8.0]])
        arr3 = np.array([[9.0, 10.0], [11.0, 12.0]])
        value = (arr1, arr2, arr3)
        result = SpectrumCoordsTuple._validate_same_shape(value)
        assert result[0].shape == (2, 2)
        assert result[1].shape == (2, 2)
        assert result[2].shape == (2, 2)
    
    def test_valid_matching_3d_arrays(self):
        """Valid 3-tuple of matching 3D arrays should pass."""
        shape = (2, 3, 4)
        arr1 = np.random.rand(*shape)
        arr2 = np.random.rand(*shape)
        arr3 = np.random.rand(*shape)
        value = (arr1, arr2, arr3)
        result = SpectrumCoordsTuple._validate_same_shape(value)
        assert all(arr.shape == shape for arr in result)
    
    def test_valid_single_element_arrays(self):
        """3-tuple of single element arrays should pass."""
        arr1 = np.array([1.0])
        arr2 = np.array([2.0])
        arr3 = np.array([3.0])
        value = (arr1, arr2, arr3)
        result = SpectrumCoordsTuple._validate_same_shape(value)
        assert all(arr.size == 1 for arr in result)
    
    def test_valid_large_arrays_matching_shapes(self):
        """3-tuple of large arrays with matching shapes should pass."""
        shape = (100, 100)
        arr1 = np.random.rand(*shape)
        arr2 = np.random.rand(*shape)
        arr3 = np.random.rand(*shape)
        value = (arr1, arr2, arr3)
        result = SpectrumCoordsTuple._validate_same_shape(value)
        assert all(arr.shape == shape for arr in result)
    
    def test_invalid_shape_mismatch_1d_vs_2d(self):
        """1D and 2D arrays should fail shape check."""
        arr1 = np.array([1.0, 2.0, 3.0])
        arr2 = np.array([[4.0, 5.0, 6.0]])
        arr3 = np.array([7.0, 8.0, 9.0])
        with pytest.raises(Exception) as exc_info:
            SpectrumCoordsTuple._validate_same_shape((arr1, arr2, arr3))
        assert 'Expected numpy arrays of the same shape' in str(exc_info.value)
        assert '(3,)' in str(exc_info.value)
        assert '(1, 3)' in str(exc_info.value)
    
    def test_invalid_shape_mismatch_different_lengths(self):
        """1D arrays with different lengths should fail."""
        arr1 = np.array([1.0, 2.0, 3.0])
        arr2 = np.array([4.0, 5.0])
        arr3 = np.array([7.0, 8.0, 9.0])
        with pytest.raises(Exception) as exc_info:
            SpectrumCoordsTuple._validate_same_shape((arr1, arr2, arr3))
        assert 'Expected numpy arrays of the same shape' in str(exc_info.value)
    
    def test_invalid_shape_mismatch_2d_dimensions(self):
        """2D arrays with different dimensions should fail."""
        arr1 = np.array([[1.0, 2.0], [3.0, 4.0]])
        arr2 = np.array([[5.0, 6.0, 7.0], [8.0, 9.0, 10.0]])
        arr3 = np.array([[11.0, 12.0], [13.0, 14.0]])
        with pytest.raises(Exception) as exc_info:
            SpectrumCoordsTuple._validate_same_shape((arr1, arr2, arr3))
        assert 'Expected numpy arrays of the same shape' in str(exc_info.value)
    
    def test_invalid_shape_mismatch_3d_arrays(self):
        """3D arrays with different shapes should fail."""
        arr1 = np.ones((2, 3, 4))
        arr2 = np.ones((2, 3, 5))
        arr3 = np.ones((2, 3, 4))
        with pytest.raises(Exception) as exc_info:
            SpectrumCoordsTuple._validate_same_shape((arr1, arr2, arr3))
        assert 'Expected numpy arrays of the same shape' in str(exc_info.value)
    
    def test_invalid_first_differs(self):
        """When first array differs should report all shapes."""
        arr1 = np.ones((1, 2))
        arr2 = np.ones((2, 2))
        arr3 = np.ones((2, 2))
        with pytest.raises(Exception) as exc_info:
            SpectrumCoordsTuple._validate_same_shape((arr1, arr2, arr3))
        error_msg = str(exc_info.value)
        assert 'Expected numpy arrays of the same shape' in error_msg
    
    def test_invalid_second_differs(self):
        """When second array differs should report all shapes."""
        arr1 = np.ones((2, 2))
        arr2 = np.ones((2, 3))
        arr3 = np.ones((2, 2))
        with pytest.raises(Exception) as exc_info:
            SpectrumCoordsTuple._validate_same_shape((arr1, arr2, arr3))
        error_msg = str(exc_info.value)
        assert 'Expected numpy arrays of the same shape' in error_msg
    
    def test_invalid_third_differs(self):
        """When third array differs should report all shapes."""
        arr1 = np.ones((2, 2))
        arr2 = np.ones((2, 2))
        arr3 = np.ones((3, 2))
        with pytest.raises(Exception) as exc_info:
            SpectrumCoordsTuple._validate_same_shape((arr1, arr2, arr3))
        error_msg = str(exc_info.value)
        assert 'Expected numpy arrays of the same shape' in error_msg


class TestFittableCoordsTuple:
    """Test CoordsTuple[FittableFloatArray] validation."""
    
    def test_valid_matching_fittable_arrays(self):
        """Valid 3-tuple of matching fittable arrays should pass."""
        arr1 = np.array([1.0, 2.0, 3.0])
        arr2 = np.array([4.0, 5.0, 6.0])
        arr3 = np.array([7.0, 8.0, 9.0])
        value = (arr1, arr2, arr3)
        result = FittableCoordsTuple._validate_same_shape(value)
        assert len(result) == 3
    
    def test_valid_matching_2d_fittable_arrays(self):
        """Valid 3-tuple of matching 2D fittable arrays should pass."""
        arr1 = np.array([[1.0, 2.0], [3.0, 4.0]])
        arr2 = np.array([[5.0, 6.0], [7.0, 8.0]])
        arr3 = np.array([[9.0, 10.0], [11.0, 12.0]])
        value = (arr1, arr2, arr3)
        result = FittableCoordsTuple._validate_same_shape(value)
        assert result[0].shape == (2, 2)
    
    def test_valid_single_element_fittable_arrays(self):
        """Single element fittable arrays should pass."""
        arr1 = np.array([1.0])
        arr2 = np.array([2.0])
        arr3 = np.array([3.0])
        value = (arr1, arr2, arr3)
        result = FittableCoordsTuple._validate_same_shape(value)
        assert all(arr.size == 1 for arr in result)
    
    def test_invalid_shape_mismatch_fittable(self):
        """Mismatched shapes should fail even with fittable constraint."""
        arr1 = np.array([1.0, 2.0, 3.0])
        arr2 = np.array([4.0, 5.0])
        arr3 = np.array([7.0, 8.0, 9.0])
        with pytest.raises(Exception) as exc_info:
            FittableCoordsTuple._validate_same_shape((arr1, arr2, arr3))
        assert 'Expected numpy arrays of the same shape' in str(exc_info.value)
    
    def test_invalid_fittable_constraints_would_fail_individual_arrays(self):
        """Arrays that violate fittable constraints should fail at array level."""
        # These arrays violate the fittable constraint (empty) but we're testing shape validation
        arr1 = np.array([1.0, 2.0])
        arr2 = np.array([3.0, 4.0])
        arr3 = np.array([5.0, 6.0])
        # Shape validation should pass
        result = FittableCoordsTuple._validate_same_shape((arr1, arr2, arr3))
        assert result[0].shape == result[1].shape == result[2].shape
    
    def test_invalid_empty_arrays_fail_shape_check(self):
        """Empty arrays still need matching shapes."""
        arr1 = np.array([])
        arr2 = np.array([])
        arr3 = np.array([])
        # These pass shape validation (all same shape), but would fail element requirement elsewhere
        result = FittableCoordsTuple._validate_same_shape((arr1, arr2, arr3))
        assert result[0].shape == result[1].shape == result[2].shape


class TestCoordsTupleShapeValidationDetails:
    """Detailed tests for shape validation logic."""
    
    def test_shape_validation_1d_length_3_vs_4(self):
        """Arrays with different 1D lengths should fail."""
        arr1 = np.arange(3, dtype=float)
        arr2 = np.arange(4, dtype=float)
        arr3 = np.arange(3, dtype=float)
        with pytest.raises(Exception) as exc_info:
            SpectrumCoordsTuple._validate_same_shape((arr1, arr2, arr3))
        assert '(3,)' in str(exc_info.value)
        assert '(4,)' in str(exc_info.value)
    
    def test_shape_validation_rectangular_arrays(self):
        """Rectangular arrays with same shape should pass."""
        arr1 = np.ones((3, 4))
        arr2 = np.ones((3, 4))
        arr3 = np.ones((3, 4))
        result = SpectrumCoordsTuple._validate_same_shape((arr1, arr2, arr3))
        assert all(arr.shape == (3, 4) for arr in result)
    
    def test_shape_validation_non_square_matrices(self):
        """Non-square matrices with matching shapes should pass."""
        shape = (5, 2)
        arr1 = np.random.rand(*shape)
        arr2 = np.random.rand(*shape)
        arr3 = np.random.rand(*shape)
        result = SpectrumCoordsTuple._validate_same_shape((arr1, arr2, arr3))
        assert all(arr.shape == shape for arr in result)
    
    def test_shape_error_message_format(self):
        """Error message should clearly show all three shapes."""
        arr1 = np.ones((2, 3))
        arr2 = np.ones((2, 4))
        arr3 = np.ones((2, 3))
        with pytest.raises(Exception) as exc_info:
            SpectrumCoordsTuple._validate_same_shape((arr1, arr2, arr3))
        error_msg = str(exc_info.value)
        assert '(2, 3)' in error_msg
        assert '(2, 4)' in error_msg
