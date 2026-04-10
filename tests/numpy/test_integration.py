"""Integration tests for numpy submodule."""

import pytest
import numpy as np
from numpy.random import RandomState

from quasar_typing.numpy import (
    FloatArray, FloatVector, FloatMatrix,
    IntArray, IntVector,
    BoolArray, BoolVector,
    FittableFloatArray, FittableFloatVector, FittableFloatMatrix,
    SortedFloatVector, SortedIntVector,
    SpectrumCoordsTuple, FittableCoordsTuple,
    RandomState_,
)


class TestValidationOrderAndPriority:
    """Test that validations happen in the correct order."""
    
    def test_array_type_check_before_dtype(self):
        """Non-array check should happen before dtype check."""
        with pytest.raises(Exception) as exc_info:
            FloatArray._validate([1.0, 2.0, 3.0])
        assert 'Expected numpy array' in str(exc_info.value)
        assert 'dtype' not in str(exc_info.value)
    
    def test_ndim_check_after_dtype(self):
        """dtype check happens before ndim check."""
        # Integer array fails dtype check before ndim check
        arr = np.array([[1, 2], [3, 4]])
        with pytest.raises(Exception) as exc_info:
            FloatMatrix._validate(arr)
        assert 'Expected numpy array of dtype' in str(exc_info.value)
    
    def test_fittable_empty_check_before_finite(self):
        """Empty check should happen before finite check."""
        arr = np.array([])
        with pytest.raises(Exception) as exc_info:
            FittableFloatArray._validate(arr)
        assert 'at least one element' in str(exc_info.value)
    
    def test_fittable_finite_check_after_empty(self):
        """Finite check happens after empty check."""
        arr = np.array([1.0, np.nan, 3.0])
        with pytest.raises(Exception) as exc_info:
            FittableFloatArray._validate(arr)
        assert 'finite values' in str(exc_info.value)


class TestMultipleConstraintsCombined:
    """Test classes with multiple constraints together."""
    
    def test_fittable_array_combines_all_constraints(self):
        """FittableFloatArray should enforce all constraints."""
        # Valid: non-empty, finite, float
        arr = np.array([1.0, 2.0, 3.0])
        result = FittableFloatArray._validate(arr)
        assert isinstance(result, np.ndarray)
        
        # Invalid: empty
        with pytest.raises(Exception):
            FittableFloatArray._validate(np.array([]))
        
        # Invalid: non-finite
        with pytest.raises(Exception):
            FittableFloatArray._validate(np.array([1.0, np.nan]))
        
        # Invalid: wrong dtype
        with pytest.raises(Exception):
            FittableFloatArray._validate(np.array([1, 2, 3]))
    
    def test_sorted_array_combines_all_constraints(self):
        """SortedFloatVector should enforce all constraints."""
        # Valid: sorted, non-empty, finite, float
        arr = np.array([1.0, 2.0, 3.0])
        result = SortedFloatVector._validate(arr)
        assert isinstance(result, np.ndarray)
        
        # Invalid: empty
        with pytest.raises(Exception):
            SortedFloatVector._validate(np.array([]))
        
        # Invalid: unsorted
        with pytest.raises(Exception):
            SortedFloatVector._validate(np.array([3.0, 1.0, 2.0]))
        
        # Invalid: non-finite
        with pytest.raises(Exception):
            SortedFloatVector._validate(np.array([1.0, np.inf]))
    
    def test_sorted_array_non_descending_order(self):
        """SortedFloatVector should accept non-descending (allowing duplicates)."""
        # Should pass: non-descending with duplicates
        arr = np.array([1.0, 2.0, 2.0, 3.0, 3.0, 3.0])
        result = SortedFloatVector._validate(arr)
        assert isinstance(result, np.ndarray)


class TestTypeAliasInheritance:
    """Test that type aliases properly inherit validator behavior."""
    
    def test_vector_aliases_differ_from_array(self):
        """Vector aliases should have different ndim than Array."""
        # FloatArray accepts any ndim, FloatVector only accepts 1
        arr1d = np.array([1.0, 2.0, 3.0])
        arr2d = np.array([[1.0, 2.0], [3.0, 4.0]])
        
        # Both should work for FloatArray
        FloatArray._validate(arr1d)
        FloatArray._validate(arr2d)
        
        # Only 1D works for FloatVector
        FloatVector._validate(arr1d)
        with pytest.raises(Exception):
            FloatVector._validate(arr2d)
    
    def test_matrix_aliases_only_2d(self):
        """Matrix aliases should only accept 2D."""
        arr1d = np.array([1.0, 2.0, 3.0])
        arr2d = np.array([[1.0, 2.0], [3.0, 4.0]])
        arr3d = np.ones((2, 2, 2), dtype=float)
        
        with pytest.raises(Exception):
            FloatMatrix._validate(arr1d)
        FloatMatrix._validate(arr2d)
        with pytest.raises(Exception):
            FloatMatrix._validate(arr3d)
    
    def test_dtype_aliases_differ(self):
        """Different dtype aliases should enforce correct dtypes."""
        int_arr = np.array([1, 2, 3])
        float_arr = np.array([1.0, 2.0, 3.0])
        bool_arr = np.array([True, False])
        
        IntArray._validate(int_arr)
        with pytest.raises(Exception):
            IntArray._validate(float_arr)
        
        FloatArray._validate(float_arr)
        with pytest.raises(Exception):
            FloatArray._validate(int_arr)
        
        BoolArray._validate(bool_arr)
        with pytest.raises(Exception):
            BoolArray._validate(int_arr)


class TestCoordsTupleWithDifferentArrayTypes:
    """Test CoordsTuple with different array type constraints."""
    
    def test_spectrum_coords_tuple_basic(self):
        """SpectrumCoordsTuple should validate basic float arrays."""
        arr1 = np.array([1.0, 2.0, 3.0])
        arr2 = np.array([4.0, 5.0, 6.0])
        arr3 = np.array([7.0, 8.0, 9.0])
        
        result = SpectrumCoordsTuple._validate_same_shape((arr1, arr2, arr3))
        assert len(result) == 3
    
    def test_spectrum_coords_tuple_allows_non_finite(self):
        """SpectrumCoordsTuple should allow non-finite values (basic arrays)."""
        arr1 = np.array([1.0, np.nan, 3.0])
        arr2 = np.array([4.0, 5.0, np.inf])
        arr3 = np.array([-np.inf, 8.0, 9.0])
        
        # Should pass shape check
        result = SpectrumCoordsTuple._validate_same_shape((arr1, arr2, arr3))
        assert len(result) == 3
    
    def test_fittable_coords_tuple_basic(self):
        """FittableCoordsTuple should validate fittable float arrays."""
        arr1 = np.array([1.0, 2.0, 3.0])
        arr2 = np.array([4.0, 5.0, 6.0])
        arr3 = np.array([7.0, 8.0, 9.0])
        
        result = FittableCoordsTuple._validate_same_shape((arr1, arr2, arr3))
        assert len(result) == 3
    
    def test_coords_tuple_shape_validation_2d(self):
        """CoordsTuple should validate shapes for 2D arrays."""
        arr1 = np.array([[1.0, 2.0], [3.0, 4.0]])
        arr2 = np.array([[5.0, 6.0], [7.0, 8.0]])
        arr3 = np.array([[9.0, 10.0], [11.0, 12.0]])
        
        result = SpectrumCoordsTuple._validate_same_shape((arr1, arr2, arr3))
        assert all(arr.shape == (2, 2) for arr in result)


class TestRandomStateValidationWithOtherTypes:
    """Test RandomState_ in context with numpy array types."""
    
    def test_random_state_separate_from_arrays(self):
        """RandomState_ should validate independently from array types."""
        rng = RandomState(42)
        result = RandomState_._validate(rng)
        assert isinstance(result, RandomState)
        
        # Can use with arrays
        arr = FloatArray._validate(rng.rand(3))
        assert isinstance(arr, np.ndarray)
    
    def test_random_state_generation_of_valid_arrays(self):
        """RandomState can generate arrays that pass our validators."""
        rng = RandomState(42)
        
        # Generate random float array
        arr = rng.randn(10)
        result = FloatVector._validate(arr)
        assert result.ndim == 1
        
        # Generate random matrix
        matrix = rng.randn(5, 5)
        result = FloatMatrix._validate(matrix)
        assert result.ndim == 2
    
    def test_random_state_generation_for_sorted_arrays(self):
        """RandomState can generate sorted arrays."""
        rng = RandomState(42)
        
        # Generate and sort
        arr = np.sort(rng.randn(10))
        result = SortedFloatVector._validate(arr)
        assert isinstance(result, np.ndarray)


class TestEdgeCases:
    """Test edge cases and boundary conditions."""    
    def test_very_large_arrays(self):
        """Very large arrays should be handled efficiently."""
        large_array = np.ones(10**7, dtype=float)
        result = FloatVector._validate(large_array)
        assert result.size == 10**7
    
    def test_high_dimensional_arrays(self):
        """High dimensional arrays should work."""
        arr = np.ones((2, 2, 2, 2, 2), dtype=float)
        result = FloatArray._validate(arr)
        assert result.ndim == 5
    
    def test_various_float_dtypes(self):
        """FloatArray should accept various floating dtypes."""
        for dtype in [np.float16, np.float32, np.float64]:
            arr = np.array([1.0, 2.0, 3.0], dtype=dtype)
            result = FloatArray._validate(arr)
            assert isinstance(result, np.ndarray)
    
    def test_various_int_dtypes(self):
        """IntArray should accept various integer dtypes."""
        for dtype in [np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64]:
            arr = np.array([1, 2, 3], dtype=dtype)
            result = IntArray._validate(arr)
            assert isinstance(result, np.ndarray)


class TestErrorMessageQuality:
    """Test that error messages are clear and helpful."""
    
    def test_dtype_error_message_helpful(self):
        """dtype error should explain what was expected vs got."""
        arr = np.array([1, 2, 3])
        with pytest.raises(Exception) as exc_info:
            FloatArray._validate(arr)
        error = str(exc_info.value)
        assert 'Expected numpy array of dtype' in error
        assert 'got' in error.lower()
    
    def test_ndim_error_message_helpful(self):
        """ndim error should explain expectations."""
        arr = np.array([[1.0, 2.0], [3.0, 4.0]])
        with pytest.raises(Exception) as exc_info:
            FloatVector._validate(arr)
        error = str(exc_info.value)
        assert 'Expected numpy array of ndim 1' in error
        assert '2' in error
    
    def test_non_finite_error_includes_count(self):
        """Non-finite error should count non-finite values."""
        arr = np.array([1.0, np.nan, np.inf, -np.inf])
        with pytest.raises(Exception) as exc_info:
            FittableFloatArray._validate(arr)
        error = str(exc_info.value)
        assert 'finite values' in error
        assert '3' in error  # 3 non-finite values
    
    def test_sorted_error_message_clear(self):
        """Sorted error should be clear about requirement."""
        arr = np.array([3.0, 1.0, 2.0])
        with pytest.raises(Exception) as exc_info:
            SortedFloatVector._validate(arr)
        error = str(exc_info.value)
        assert 'sorted' in error.lower()
    
    def test_shape_mismatch_error_shows_all_shapes(self):
        """CoordsTuple error should show all three shape mismatches."""
        arr1 = np.ones((2, 3))
        arr2 = np.ones((2, 4))
        arr3 = np.ones((3, 3))
        with pytest.raises(Exception) as exc_info:
            SpectrumCoordsTuple._validate_same_shape((arr1, arr2, arr3))
        error = str(exc_info.value)
        assert '(2, 3)' in error
        assert '(2, 4)' in error
        assert '(3, 3)' in error
