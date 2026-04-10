"""Unit tests for SortedArray_ type aliases."""

import pytest
import numpy as np

from quasar_typing.numpy import SortedFloatVector, SortedIntVector


class TestSortedFloatVector:
    """Test SortedArray_ validation for sorted float arrays."""
    
    def test_valid_sorted_ascending_vector(self):
        """Valid ascending sorted vector should pass validation."""
        arr = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        result = SortedFloatVector._validate(arr)
        assert isinstance(result, np.ndarray)
        np.testing.assert_array_equal(result, arr)
    
    def test_valid_sorted_with_decimals(self):
        """Sorted vector with decimal values should pass."""
        arr = np.array([0.1, 0.5, 1.2, 5.3, 10.2])
        result = SortedFloatVector._validate(arr)
        assert (np.diff(result) >= 0).all()
    
    def test_valid_single_element(self):
        """Single element vector should pass."""
        arr = np.array([42.0])
        result = SortedFloatVector._validate(arr)
        assert result.size == 1
    
    def test_valid_two_element_sorted(self):
        """Two element sorted vector should pass."""
        arr = np.array([1.0, 2.0])
        result = SortedFloatVector._validate(arr)
        assert result.size == 2
    
    def test_valid_negative_values_sorted(self):
        """Sorted vector with negative values should pass."""
        arr = np.array([-10.0, -5.0, -1.0, 0.0, 1.0])
        result = SortedFloatVector._validate(arr)
        assert isinstance(result, np.ndarray)
    
    def test_valid_all_identical_values(self):
        """Vector with all identical values should pass (non-descending order)."""
        arr = np.array([5.0, 5.0, 5.0, 5.0])
        result = SortedFloatVector._validate(arr)
        assert isinstance(result, np.ndarray)
    
    def test_valid_duplicates_at_beginning(self):
        """Sorted vector with duplicates at beginning should pass."""
        arr = np.array([1.0, 1.0, 2.0, 3.0])
        result = SortedFloatVector._validate(arr)
        assert isinstance(result, np.ndarray)
    
    def test_valid_duplicates_at_end(self):
        """Sorted vector with duplicates at end should pass."""
        arr = np.array([1.0, 2.0, 3.0, 3.0])
        result = SortedFloatVector._validate(arr)
        assert isinstance(result, np.ndarray)
    
    def test_valid_duplicates_in_middle(self):
        """Sorted vector with duplicates in middle should pass."""
        arr = np.array([1.0, 2.0, 2.0, 3.0])
        result = SortedFloatVector._validate(arr)
        assert isinstance(result, np.ndarray)
    
    def test_invalid_non_array_input(self):
        """Non-array input should raise error."""
        with pytest.raises(Exception) as exc_info:
            SortedFloatVector._validate([1.0, 2.0, 3.0])
        assert 'Expected numpy array' in str(exc_info.value)
    
    def test_invalid_empty_vector(self):
        """Empty vector should raise error (must have at least one element)."""
        arr = np.array([])
        with pytest.raises(Exception) as exc_info:
            SortedFloatVector._validate(arr)
        assert 'Expected numpy array with at least one element' in str(exc_info.value)
    
    def test_invalid_unsorted_vector(self):
        """Unsorted vector should raise error."""
        arr = np.array([1.0, 3.0, 2.0, 4.0])
        with pytest.raises(Exception) as exc_info:
            SortedFloatVector._validate(arr)
        assert 'Expected numpy array sorted in non-descending order' in str(exc_info.value)
    
    def test_invalid_reverse_sorted_vector(self):
        """Reverse sorted vector should raise error."""
        arr = np.array([5.0, 4.0, 3.0, 2.0, 1.0])
        with pytest.raises(Exception) as exc_info:
            SortedFloatVector._validate(arr)
        assert 'Expected numpy array sorted in non-descending order' in str(exc_info.value)
    
    def test_invalid_partially_sorted(self):
        """Partially sorted vector should raise error."""
        arr = np.array([1.0, 2.0, 3.0, 2.5, 4.0])
        with pytest.raises(Exception) as exc_info:
            SortedFloatVector._validate(arr)
        assert 'Expected numpy array sorted in non-descending order' in str(exc_info.value)
    
    def test_invalid_2d_array(self):
        """2D array should fail ndim check (must be 1D)."""
        arr = np.array([[1.0, 2.0], [3.0, 4.0]])
        with pytest.raises(Exception) as exc_info:
            SortedFloatVector._validate(arr)
        assert 'Expected numpy array of ndim 1' in str(exc_info.value)
    
    def test_invalid_with_nan(self):
        """Vector with NaN should raise error (fails finite check)."""
        arr = np.array([1.0, np.nan, 3.0])
        with pytest.raises(Exception) as exc_info:
            SortedFloatVector._validate(arr)
        assert 'Expected numpy array with finite values' in str(exc_info.value)
    
    def test_invalid_with_inf(self):
        """Vector with inf should raise error (fails finite check)."""
        arr = np.array([1.0, np.inf, 3.0])
        with pytest.raises(Exception) as exc_info:
            SortedFloatVector._validate(arr)
        assert 'Expected numpy array with finite values' in str(exc_info.value)
    
    def test_invalid_with_neg_inf(self):
        """Vector with negative inf should raise error."""
        arr = np.array([-np.inf, 0.0, 1.0])
        with pytest.raises(Exception) as exc_info:
            SortedFloatVector._validate(arr)
        assert 'Expected numpy array with finite values' in str(exc_info.value)
    
    def test_integer_array(self):
        """Integer array should fail dtype check."""
        arr = np.array([1, 2, 3], dtype=np.int64)
        with pytest.raises(Exception) as exc_info:
            SortedFloatVector._validate(arr)
        assert 'Expected numpy array of dtype' in str(exc_info.value)
    
    def test_validation_order_non_empty_before_sorted(self):
        """Empty check should happen before sorted check."""
        arr = np.array([])
        with pytest.raises(Exception) as exc_info:
            SortedFloatVector._validate(arr)
        assert 'at least one element' in str(exc_info.value)


class TestSortedIntVector:
    """Test SortedArray_ validation for sorted integer arrays."""
    
    def test_valid_sorted_int_vector(self):
        """Valid sorted integer vector should pass."""
        arr = np.array([1, 2, 3, 4, 5])
        result = SortedIntVector._validate(arr)
        assert isinstance(result, np.ndarray)
    
    def test_valid_single_element(self):
        """Single element integer vector should pass."""
        arr = np.array([42])
        result = SortedIntVector._validate(arr)
        assert result.size == 1
    
    def test_valid_negative_sorted_integers(self):
        """Sorted vector with negative integers should pass."""
        arr = np.array([-10, -5, -1, 0, 1])
        result = SortedIntVector._validate(arr)
        assert isinstance(result, np.ndarray)
    
    def test_valid_duplicate_integers(self):
        """Sorted vector with duplicate integers should pass."""
        arr = np.array([1, 1, 2, 2, 3])
        result = SortedIntVector._validate(arr)
        assert isinstance(result, np.ndarray)
    
    def test_invalid_unsorted_int_vector(self):
        """Unsorted integer vector should raise error."""
        arr = np.array([1, 3, 2, 4])
        with pytest.raises(Exception) as exc_info:
            SortedIntVector._validate(arr)
        assert 'Expected numpy array' in str(exc_info.value) and 'sorted' in str(exc_info.value)
    
    def test_invalid_empty_int_vector(self):
        """Empty integer vector should raise error."""
        arr = np.array([], dtype=int)
        with pytest.raises(Exception) as exc_info:
            SortedIntVector._validate(arr)
        assert 'Expected numpy array with at least one element' in str(exc_info.value)
    
    def test_invalid_reverse_sorted_int_vector(self):
        """Reverse sorted integer vector should raise error."""
        arr = np.array([5, 4, 3, 2, 1])
        with pytest.raises(Exception) as exc_info:
            SortedIntVector._validate(arr)
        assert 'Expected numpy array' in str(exc_info.value) and 'sorted' in str(exc_info.value)
    
    def test_invalid_float_array(self):
        """Float array should fail dtype check."""
        arr = np.array([1.0, 2.0, 3.0])
        with pytest.raises(Exception) as exc_info:
            SortedIntVector._validate(arr)
        assert 'Expected numpy array of dtype' in str(exc_info.value)
    
    def test_invalid_2d_int_array(self):
        """2D array should fail ndim check."""
        arr = np.array([[1, 2], [3, 4]])
        with pytest.raises(Exception) as exc_info:
            SortedIntVector._validate(arr)
        assert 'Expected numpy array of ndim 1' in str(exc_info.value)
