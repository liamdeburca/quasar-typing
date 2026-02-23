"""Unit tests for numpy module validations."""

import pytest
import numpy as np
from numpy.random import RandomState

from quasar_typing.numpy import (
    FloatArray, FloatVector, FloatMatrix, FloatCube,
    IntArray, IntVector, 
    BoolArray, BoolVector, BoolMatrix, BoolCube,
    FittableFloatArray, FittableFloatVector, FittableFloatMatrix, FittableFloatCube,
    SortedFloatVector,
)
from quasar_typing.numpy.random_state import RandomState_

# ============================================================================
# Array_ Tests
# ============================================================================

class TestFloatArray:
    """Test Array_ validation for floating point arrays."""
    
    def test_valid_float_array(self):
        """Valid float array should pass validation."""
        arr = np.array([1.0, 2.0, 3.0])
        result = FloatArray._validate(arr)
        assert isinstance(result, np.ndarray)
        np.testing.assert_array_equal(result, arr)
    
    def test_valid_float_array_2d(self):
        """Valid 2D float array should pass validation."""
        arr = np.array([[1.0, 2.0], [3.0, 4.0]])
        result = FloatArray._validate(arr)
        assert result.ndim == 2
        assert result.shape == (2, 2)
    
    def test_invalid_non_array_input(self):
        """Non-array input should raise error."""
        with pytest.raises(Exception) as exc_info:
            FloatArray._validate([1.0, 2.0, 3.0])
        assert 'Expected numpy array' in str(exc_info.value)
    
    def test_invalid_tuple_input(self):
        """Tuple input should raise error."""
        with pytest.raises(Exception):
            FloatArray._validate((1.0, 2.0, 3.0))
    
    def test_invalid_string_input(self):
        """String input should raise error."""
        with pytest.raises(Exception):
            FloatArray._validate("not an array")
    
    def test_invalid_int_input(self):
        """Integer input should raise error."""
        with pytest.raises(Exception):
            FloatArray._validate(42)

class TestFloatVector:
    """Test Array_ validation for 1D float arrays."""
    
    def test_valid_1d_array(self):
        """Valid 1D float array should pass validation."""
        arr = np.array([1.0, 2.0, 3.0])
        result = FloatVector._validate(arr)
        assert result.ndim == 1
    
    def test_invalid_2d_array(self):
        """2D array should fail for FloatVector."""
        arr = np.array([[1.0, 2.0], [3.0, 4.0]])
        with pytest.raises(Exception) as exc_info:
            FloatVector._validate(arr)
        assert 'Expected numpy array of ndim 1' in str(exc_info.value)
    
    def test_invalid_3d_array(self):
        """3D array should fail for FloatVector."""
        arr = np.array([[[1.0, 2.0]]])
        with pytest.raises(Exception) as exc_info:
            FloatVector._validate(arr)
        assert 'Expected numpy array of ndim 1' in str(exc_info.value)

class TestFloatMatrix:
    """Test Array_ validation for 2D float arrays."""
    
    def test_valid_2d_array(self):
        """Valid 2D float array should pass validation."""
        arr = np.array([[1.0, 2.0], [3.0, 4.0]])
        result = FloatMatrix._validate(arr)
        assert result.ndim == 2
    
    def test_invalid_1d_array(self):
        """1D array should fail for FloatMatrix."""
        arr = np.array([1.0, 2.0, 3.0])
        with pytest.raises(Exception) as exc_info:
            FloatMatrix._validate(arr)
        assert 'Expected numpy array of ndim 2' in str(exc_info.value)
    
    def test_invalid_3d_array(self):
        """3D array should fail for FloatMatrix."""
        arr = np.array([[[1.0, 2.0]]])
        with pytest.raises(Exception):
            FloatMatrix._validate(arr)

class TestFloatCube:
    """Test Array_ validation for 3D float arrays."""
    
    def test_valid_3d_array(self):
        """Valid 3D float array should pass validation."""
        arr = np.array([[[1.0, 2.0]]])
        result = FloatCube._validate(arr)
        assert result.ndim == 3
    
    def test_invalid_1d_array(self):
        """1D array should fail for FloatCube."""
        arr = np.array([1.0, 2.0, 3.0])
        with pytest.raises(Exception):
            FloatCube._validate(arr)
    
    def test_invalid_2d_array(self):
        """2D array should fail for FloatCube."""
        arr = np.array([[1.0, 2.0], [3.0, 4.0]])
        with pytest.raises(Exception):
            FloatCube._validate(arr)

class TestIntArray:
    """Test Array_ validation for integer arrays."""
    
    def test_valid_int_array(self):
        """Valid integer array should pass validation."""
        arr = np.array([1, 2, 3])
        result = IntArray._validate(arr)
        assert isinstance(result, np.ndarray)
        np.testing.assert_array_equal(result, arr)
    
    def test_invalid_float_array(self):
        """Float array should fail for IntArray."""
        arr = np.array([1.5, 2.5, 3.5])
        with pytest.raises(Exception) as exc_info:
            IntArray._validate(arr)
        assert 'Expected numpy array of dtype' in str(exc_info.value)

class TestIntVector:
    """Test Array_ validation for 1D integer arrays."""
    
    def test_valid_1d_int_array(self):
        """Valid 1D integer array should pass validation."""
        arr = np.array([1, 2, 3])
        result = IntVector._validate(arr)
        assert result.ndim == 1
    
    def test_invalid_float_1d_array(self):
        """Float 1D array should fail for IntVector."""
        arr = np.array([1.0, 2.0, 3.0])
        with pytest.raises(Exception):
            IntVector._validate(arr)

class TestBoolArray:
    """Test Array_ validation for boolean arrays."""
    
    def test_valid_bool_array(self):
        """Valid boolean array should pass validation."""
        arr = np.array([True, False, True])
        result = BoolArray._validate(arr)
        assert isinstance(result, np.ndarray)
    
    def test_invalid_int_array(self):
        """Integer array should fail for BoolArray."""
        arr = np.array([1, 0, 1])
        with pytest.raises(Exception) as exc_info:
            BoolArray._validate(arr)
        assert 'Expected numpy array of dtype' in str(exc_info.value)

class TestBoolVector:
    """Test Array_ validation for 1D boolean arrays."""
    
    def test_valid_1d_bool_array(self):
        """Valid 1D boolean array should pass validation."""
        arr = np.array([True, False, True])
        result = BoolVector._validate(arr)
        assert result.ndim == 1

class TestBoolMatrix:
    """Test Array_ validation for 2D boolean arrays."""
    
    def test_valid_2d_bool_array(self):
        """Valid 2D boolean array should pass validation."""
        arr = np.array([[True, False], [False, True]])
        result = BoolMatrix._validate(arr)
        assert result.ndim == 2

class TestBoolCube:
    """Test Array_ validation for 3D boolean arrays."""
    
    def test_valid_3d_bool_array(self):
        """Valid 3D boolean array should pass validation."""
        arr = np.array([[[True, False]]])
        result = BoolCube._validate(arr)
        assert result.ndim == 3

# ============================================================================
# FittableArray_ Tests
# ============================================================================

class TestFittableFloatArray:
    """Test FittableArray_ validation for floating point arrays."""
    
    def test_valid_fittable_array(self):
        """Valid fittable array with finite values should pass validation."""
        arr = np.array([1.0, 2.0, 3.0])
        result = FittableFloatArray._validate(arr)
        assert isinstance(result, np.ndarray)
    
    def test_valid_fittable_array_2d(self):
        """Valid 2D fittable array should pass validation."""
        arr = np.array([[1.0, 2.0], [3.0, 4.0]])
        result = FittableFloatArray._validate(arr)
        assert result.ndim == 2
    
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
    
    def test_invalid_array_with_nan(self):
        """Array with NaN values should raise error."""
        arr = np.array([1.0, np.nan, 3.0])
        with pytest.raises(Exception) as exc_info:
            FittableFloatArray._validate(arr)
        assert 'Expected numpy array with finite values' in str(exc_info.value)
        assert '1 non-finite' in str(exc_info.value)
    
    def test_invalid_array_with_inf(self):
        """Array with inf values should raise error."""
        arr = np.array([1.0, np.inf, 3.0])
        with pytest.raises(Exception) as exc_info:
            FittableFloatArray._validate(arr)
        assert 'Expected numpy array with finite values' in str(exc_info.value)
    
    def test_invalid_array_with_negative_inf(self):
        """Array with negative inf values should raise error."""
        arr = np.array([1.0, -np.inf, 3.0])
        with pytest.raises(Exception) as exc_info:
            FittableFloatArray._validate(arr)
        assert 'Expected numpy array with finite values' in str(exc_info.value)
    
    def test_invalid_array_with_multiple_non_finite(self):
        """Array with multiple non-finite values should report count."""
        arr = np.array([1.0, np.nan, np.inf, -np.inf, 5.0])
        with pytest.raises(Exception) as exc_info:
            FittableFloatArray._validate(arr)
        error_msg = str(exc_info.value)
        assert 'Expected numpy array with finite values' in error_msg
        assert '3 non-finite' in error_msg

class TestFittableFloatVector:
    """Test FittableArray_ validation for 1D floating point arrays."""
    
    def test_valid_fittable_vector(self):
        """Valid fittable 1D array should pass validation."""
        arr = np.array([1.0, 2.0, 3.0])
        result = FittableFloatVector._validate(arr)
        assert result.ndim == 1
    
    def test_invalid_empty_vector(self):
        """Empty vector should raise error."""
        arr = np.array([])
        with pytest.raises(Exception) as exc_info:
            FittableFloatVector._validate(arr)
        assert 'Expected numpy array with at least one element' in str(exc_info.value)
    
    def test_invalid_vector_with_nan(self):
        """Vector with NaN should raise error."""
        arr = np.array([1.0, np.nan, 3.0])
        with pytest.raises(Exception):
            FittableFloatVector._validate(arr)
    
    def test_invalid_2d_array(self):
        """2D array should fail for FittableFloatVector."""
        arr = np.array([[1.0, 2.0], [3.0, 4.0]])
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
    
    def test_invalid_empty_matrix(self):
        """Empty matrix should raise error."""
        arr = np.empty((0, 2))
        with pytest.raises(Exception):
            FittableFloatMatrix._validate(arr)
    
    def test_invalid_matrix_with_nan(self):
        """Matrix with NaN should raise error."""
        arr = np.array([[1.0, np.nan], [3.0, 4.0]])
        with pytest.raises(Exception):
            FittableFloatMatrix._validate(arr)
    
    def test_invalid_1d_array(self):
        """1D array should fail for FittableFloatMatrix."""
        arr = np.array([1.0, 2.0, 3.0])
        with pytest.raises(Exception):
            FittableFloatMatrix._validate(arr)

class TestFittableFloatCube:
    """Test FittableArray_ validation for 3D floating point arrays."""
    
    def test_valid_fittable_cube(self):
        """Valid fittable 3D array should pass validation."""
        arr = np.array([[[1.0, 2.0]]])
        result = FittableFloatCube._validate(arr)
        assert result.ndim == 3
    
    def test_invalid_empty_cube(self):
        """Empty cube should raise error."""
        arr = np.empty((0, 2, 2))
        with pytest.raises(Exception):
            FittableFloatCube._validate(arr)
    
    def test_invalid_cube_with_inf(self):
        """Cube with inf should raise error."""
        arr = np.array([[[1.0, np.inf]]])
        with pytest.raises(Exception):
            FittableFloatCube._validate(arr)

# ============================================================================
# SortedArray_ Tests
# ============================================================================

class TestSortedFloatVector:
    """Test SortedArray_ validation for sorted float arrays."""
    
    def test_valid_sorted_vector(self):
        """Valid sorted vector should pass validation."""
        arr = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        result = SortedFloatVector._validate(arr)
        assert isinstance(result, np.ndarray)
    
    def test_valid_sorted_vector_floats(self):
        """Valid sorted float vector should pass validation."""
        arr = np.array([0.1, 0.5, 1.2, 5.3, 10.2])
        result = SortedFloatVector._validate(arr)
        assert (np.diff(result) > 0).all()
    
    def test_invalid_non_array_input(self):
        """Non-array input should raise error."""
        with pytest.raises(Exception) as exc_info:
            SortedFloatVector._validate([1.0, 2.0, 3.0])
        assert 'Expected numpy array' in str(exc_info.value)
    
    def test_invalid_empty_vector(self):
        """Empty vector should raise error."""
        arr = np.array([])
        with pytest.raises(Exception) as exc_info:
            SortedFloatVector._validate(arr)
        assert 'Expected numpy array with at least one element' in str(exc_info.value)
    
    def test_invalid_unsorted_vector(self):
        """Unsorted vector should raise error."""
        arr = np.array([1.0, 3.0, 2.0, 4.0])
        with pytest.raises(Exception) as exc_info:
            SortedFloatVector._validate(arr)
        assert 'Expected sorted numpy array' in str(exc_info.value)
    
    def test_invalid_reverse_sorted_vector(self):
        """Reverse sorted vector should raise error."""
        arr = np.array([5.0, 4.0, 3.0, 2.0, 1.0])
        with pytest.raises(Exception) as exc_info:
            SortedFloatVector._validate(arr)
        assert 'Expected sorted numpy array' in str(exc_info.value)
    
    def test_invalid_duplicate_values(self):
        """Vector with duplicate values should raise error."""
        arr = np.array([1.0, 2.0, 2.0, 3.0])
        with pytest.raises(Exception) as exc_info:
            SortedFloatVector._validate(arr)
        assert 'Expected sorted numpy array' in str(exc_info.value)
    
    def test_valid_single_element(self):
        """Single element array should pass validation."""
        arr = np.array([42.0])
        result = SortedFloatVector._validate(arr)
        assert result.size == 1
    
    def test_valid_two_element_sorted(self):
        """Two element sorted array should pass validation."""
        arr = np.array([1.0, 2.0])
        result = SortedFloatVector._validate(arr)
        assert result.size == 2

# ============================================================================
# RandomState_ Tests
# ============================================================================

class TestRandomState:
    """Test RandomState_ validation."""
    
    def test_valid_random_state(self):
        """Valid RandomState should pass validation."""
        rng = RandomState(42)
        result = RandomState_._validate(rng)
        assert isinstance(result, RandomState)
    
    def test_valid_random_state_with_seed(self):
        """RandomState with seed should pass validation."""
        rng = RandomState(12345)
        result = RandomState_._validate(rng)
        assert isinstance(result, RandomState)
    
    def test_invalid_integer_input(self):
        """Integer input should raise error."""
        with pytest.raises(Exception) as exc_info:
            RandomState_._validate(42)
        assert 'Expected numpy RandomState' in str(exc_info.value)
    
    def test_invalid_none_input(self):
        """None input should raise error."""
        with pytest.raises(Exception) as exc_info:
            RandomState_._validate(None)
        assert 'Expected numpy RandomState' in str(exc_info.value)
    
    def test_invalid_list_input(self):
        """List input should raise error."""
        with pytest.raises(Exception) as exc_info:
            RandomState_._validate([1, 2, 3])
        assert 'Expected numpy RandomState' in str(exc_info.value)
    
    def test_invalid_numpy_generator(self):
        """NumPy's Generator should not pass RandomState_ validation."""
        rng = np.random.default_rng(42)
        with pytest.raises(Exception) as exc_info:
            RandomState_._validate(rng)
        assert 'Expected numpy RandomState' in str(exc_info.value)

# ============================================================================
# Integration Tests
# ============================================================================

class TestDirectValidationIntegration:
    """Integration tests combining multiple validations."""
    
    def test_fittable_with_all_validations(self):
        """Test FittableFloatVector with all validations combined."""
        # Should pass: non-empty, finite, 1D
        result = FittableFloatVector._validate(np.array([1.0, 2.0, 3.0]))
        assert result.size == 3
        
        # Should fail: empty
        with pytest.raises(Exception):
            FittableFloatVector._validate(np.array([]))
        
        # Should fail: non-finite
        with pytest.raises(Exception):
            FittableFloatVector._validate(np.array([1.0, np.nan]))
        
        # Should fail: wrong ndim
        with pytest.raises(Exception):
            FittableFloatVector._validate(np.array([[1.0, 2.0]]))
    
    def test_sorted_with_all_validations(self):
        """Test SortedFloatVector with all validations combined."""
        # Should pass: sorted, non-empty
        result = SortedFloatVector._validate(np.array([1.0, 2.0, 3.0]))
        assert result.size == 3
        
        # Should fail: empty
        with pytest.raises(Exception):
            SortedFloatVector._validate(np.array([]))
        
        # Should fail: unsorted
        with pytest.raises(Exception):
            SortedFloatVector._validate(np.array([3.0, 1.0, 2.0]))
    
    def test_validation_order_matters(self):
        """Test that validations are checked in correct order."""
        # For FittableArray, non-array check happens first
        with pytest.raises(Exception) as exc_info:
            FittableFloatArray._validate([1.0, 2.0])
        assert 'Expected numpy array' in str(exc_info.value)
        
        # Empty check happens before finite check
        with pytest.raises(Exception) as exc_info:
            FittableFloatArray._validate(np.array([]))
        assert 'at least one element' in str(exc_info.value)