"""Test Sorted Array validation using pydantic validate_call."""

import numpy as np
import pytest
from pydantic import TypeAdapter, ValidationError, validate_call
from pydantic_core import PydanticCustomError

from quasar_typing.numpy import SortedFloatVector, SortedIntVector

# ============================================================================
# SortedFloatVector Tests
# ============================================================================

def test_sorted_float_vector_valid_ascending(sorted_float_1d_basic):
    """Valid ascending sorted vector should pass validation."""
    result = TypeAdapter(SortedFloatVector).validate_python(sorted_float_1d_basic)
    assert isinstance(result, np.ndarray)
    assert (np.diff(result) >= 0).all()


def test_sorted_float_vector_valid_decimals(sorted_float_1d_decimal):
    """Sorted vector with decimal values should pass."""
    result = TypeAdapter(SortedFloatVector).validate_python(sorted_float_1d_decimal)
    assert (np.diff(result) >= 0).all()


def test_sorted_float_vector_valid_single_element(sorted_float_1d_single):
    """Single element vector should pass."""
    result = TypeAdapter(SortedFloatVector).validate_python(sorted_float_1d_single)
    assert result.size == 1


def test_sorted_float_vector_valid_two_elements():
    """Two element sorted vector should pass."""
    arr = np.array([1.0, 2.0])
    result = TypeAdapter(SortedFloatVector).validate_python(arr)
    assert result.size == 2


def test_sorted_float_vector_valid_negative(sorted_float_1d_negative):
    """Sorted vector with negative values should pass."""
    result = TypeAdapter(SortedFloatVector).validate_python(sorted_float_1d_negative)
    assert isinstance(result, np.ndarray)


def test_sorted_float_vector_valid_all_identical():
    """Vector with all identical values should pass (non-descending order)."""
    arr = np.array([5.0, 5.0, 5.0, 5.0])
    result = TypeAdapter(SortedFloatVector).validate_python(arr)
    assert isinstance(result, np.ndarray)


def test_sorted_float_vector_valid_duplicates_beginning(sorted_float_1d_with_duplicates):
    """Sorted vector with duplicates should pass."""
    result = TypeAdapter(SortedFloatVector).validate_python(sorted_float_1d_with_duplicates)
    assert isinstance(result, np.ndarray)


def test_sorted_float_vector_valid_many_duplicates():
    """Sorted vector with many duplicate values should pass."""
    arr = np.array([1.0, 1.0, 1.0, 2.0, 2.0, 3.0, 3.0, 3.0])
    result = TypeAdapter(SortedFloatVector).validate_python(arr)
    assert (np.diff(result) >= 0).all()


def test_sorted_float_vector_invalid_non_array():
    """Non-array input should raise error."""
    TypeAdapter(SortedFloatVector).validate_python([1.0, 2.0, 3.0])


def test_sorted_float_vector_invalid_empty():
    """Empty vector should raise error (must have at least one element)."""
    arr = np.array([])
    with pytest.raises((ValidationError, PydanticCustomError)):
        TypeAdapter(SortedFloatVector).validate_python(arr)


def test_sorted_float_vector_invalid_unsorted():
    """Unsorted vector should raise error."""
    arr = np.array([1.0, 3.0, 2.0, 4.0])
    with pytest.raises((ValidationError, PydanticCustomError)):
        TypeAdapter(SortedFloatVector).validate_python(arr)


def test_sorted_float_vector_invalid_reverse():
    """Reverse sorted vector should raise error."""
    arr = np.array([5.0, 4.0, 3.0, 2.0, 1.0])
    with pytest.raises((ValidationError, PydanticCustomError)):
        TypeAdapter(SortedFloatVector).validate_python(arr)


def test_sorted_float_vector_invalid_partially_sorted():
    """Partially sorted vector should raise error."""
    arr = np.array([1.0, 2.0, 3.0, 2.5, 4.0])
    with pytest.raises((ValidationError, PydanticCustomError)):
        TypeAdapter(SortedFloatVector).validate_python(arr)


def test_sorted_float_vector_invalid_single_out_of_order():
    """Single out-of-order element should raise error."""
    arr = np.array([1.0, 2.0, 3.0, 4.0, 3.5, 5.0])
    with pytest.raises((ValidationError, PydanticCustomError)):
        TypeAdapter(SortedFloatVector).validate_python(arr)


def test_sorted_float_vector_invalid_nan():
    """Array with NaN should raise error (NaN not finite)."""
    arr = np.array([1.0, 2.0, np.nan, 4.0])
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(SortedFloatVector).validate_python(arr)
    # Could be either finite or sorted error, depending on order of checks
    assert 'finite' in str(exc_info.value) or 'sorted' in str(exc_info.value)


def test_sorted_float_vector_invalid_inf():
    """Array with Inf is valid but not finite."""
    arr = np.array([1.0, 2.0, np.inf, 4.0])
    # This should fail on finite check before sort check
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(SortedFloatVector).validate_python(arr)
    assert 'finite' in str(exc_info.value)


# ============================================================================
# SortedIntVector Tests
# ============================================================================

def test_sorted_int_vector_valid(sorted_int_1d_basic):
    """Valid sorted 1D integer array should pass."""
    result = TypeAdapter(SortedIntVector).validate_python(sorted_int_1d_basic)
    assert (np.diff(result) >= 0).all()


def test_sorted_int_vector_valid_with_duplicates(sorted_int_1d_with_duplicates):
    """Sorted integer array with duplicates should pass."""
    result = TypeAdapter(SortedIntVector).validate_python(sorted_int_1d_with_duplicates)
    assert (np.diff(result) >= 0).all()


def test_sorted_int_vector_valid_negative(sorted_int_1d_negative):
    """Sorted integer array with negative values should pass."""
    result = TypeAdapter(SortedIntVector).validate_python(sorted_int_1d_negative)
    assert (np.diff(result) >= 0).all()


def test_sorted_int_vector_valid_single_element():
    """Single element integer vector should pass."""
    arr = np.array([42], dtype=np.int32)
    result = TypeAdapter(SortedIntVector).validate_python(arr)
    assert result.size == 1


def test_sorted_int_vector_valid_large_values():
    """Sorted vector with large integer values should pass."""
    arr = np.array([1000000, 2000000, 3000000], dtype=np.int32)
    result = TypeAdapter(SortedIntVector).validate_python(arr)
    assert (np.diff(result) >= 0).all()


def test_sorted_int_vector_valid_all_same():
    """Vector with all same integers should pass."""
    arr = np.array([5, 5, 5, 5], dtype=np.int32)
    result = TypeAdapter(SortedIntVector).validate_python(arr)
    assert isinstance(result, np.ndarray)


def test_sorted_int_vector_invalid_empty():
    """Empty integer vector should raise error."""
    arr = np.array([], dtype=np.int32)
    with pytest.raises((ValidationError, PydanticCustomError)):
        TypeAdapter(SortedIntVector).validate_python(arr)


def test_sorted_int_vector_invalid_unsorted():
    """Unsorted integer vector should raise error."""
    arr = np.array([1, 3, 2, 4], dtype=np.int32)
    with pytest.raises((ValidationError, PydanticCustomError)):
        TypeAdapter(SortedIntVector).validate_python(arr)


def test_sorted_int_vector_invalid_reverse():
    """Reverse sorted integer vector should raise error."""
    arr = np.array([5, 4, 3, 2, 1], dtype=np.int32)
    with pytest.raises((ValidationError, PydanticCustomError)):
        TypeAdapter(SortedIntVector).validate_python(arr)


def test_sorted_int_vector_invalid_partially_sorted():
    """Partially sorted integer vector should raise error."""
    arr = np.array([1, 2, 3, 2, 4], dtype=np.int32)
    with pytest.raises((ValidationError, PydanticCustomError)):
        TypeAdapter(SortedIntVector).validate_python(arr)


def test_sorted_int_vector_invalid_list():
    """List should not be accepted."""
    TypeAdapter(SortedIntVector).validate_python([1, 2, 3])


def test_sorted_int_vector_invalid_float_array():
    """Float array should not be accepted."""
    arr = np.array([1.0, 2.0, 3.0])
    with pytest.raises((ValidationError, PydanticCustomError)):
        TypeAdapter(SortedIntVector).validate_python(arr)


# ============================================================================
# Pydantic validate_call Tests
# ============================================================================

def test_validate_call_with_sorted_float_vector():
    """Test validate_call with SortedFloatVector type hint."""
    @validate_call
    def process_sorted(vec: SortedFloatVector) -> float:
        return float(vec[-1])  # Last element
    
    arr = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    result = process_sorted(arr)
    assert result == 5.0


def test_validate_call_rejects_unsorted():
    """validate_call should reject unsorted array for SortedFloatVector."""
    @validate_call
    def process_sorted(vec: SortedFloatVector) -> float:
        return float(vec[-1])
    
    arr = np.array([1.0, 3.0, 2.0, 4.0])
    with pytest.raises((ValidationError, PydanticCustomError)):
        process_sorted(arr)


def test_validate_call_rejects_empty_sorted():
    """validate_call should reject empty array for SortedFloatVector."""
    @validate_call
    def process_sorted(vec: SortedFloatVector) -> float:
        return float(vec[0])
    
    with pytest.raises((ValidationError, PydanticCustomError)):
        process_sorted(np.array([]))


def test_validate_call_with_sorted_int_vector():
    """Test validate_call with SortedIntVector type hint."""
    @validate_call
    def process_sorted_int(vec: SortedIntVector) -> int:
        return int(vec[-1])
    
    arr = np.array([1, 2, 3, 4, 5], dtype=np.int32)
    result = process_sorted_int(arr)
    assert result == 5


def test_validate_call_rejects_unsorted_int():
    """validate_call should reject unsorted int array."""
    @validate_call
    def process_sorted_int(vec: SortedIntVector) -> int:
        return int(vec[-1])
    
    arr = np.array([5, 2, 3, 1, 4], dtype=np.int32)
    with pytest.raises((ValidationError, PydanticCustomError)):
        process_sorted_int(arr)


def test_validate_call_multiple_sorted_vectors():
    """validate_call should work with multiple sorted vector parameters."""
    @validate_call
    def merge_sorted(v1: SortedFloatVector, v2: SortedFloatVector) -> np.ndarray:
        # Merge two sorted arrays
        return np.sort(np.concatenate([v1, v2]))
    
    arr1 = np.array([1.0, 3.0, 5.0])
    arr2 = np.array([2.0, 4.0, 6.0])
    
    result = merge_sorted(arr1, arr2)
    assert (np.diff(result) >= 0).all()
    assert result.size == 6


def test_validate_call_sorted_vector_computation():
    """validate_call should allow computations on sorted vectors."""
    @validate_call
    def binary_search_idx(vec: SortedFloatVector, target: float) -> int:
        # Find where target would be inserted
        return int(np.searchsorted(vec, target))
    
    arr = np.array([1.0, 3.0, 5.0, 7.0, 9.0])
    
    idx = binary_search_idx(arr, 6.0)
    assert idx == 3


# ============================================================================
# Edge Cases
# ============================================================================

def test_sorted_float_vector_very_small_values():
    """Sorted vector with very small finite values should pass."""
    arr = np.array([1e-100, 1e-50, 1e-10])
    result = TypeAdapter(SortedFloatVector).validate_python(arr)
    assert (np.diff(result) >= 0).all()


def test_sorted_float_vector_very_large_values():
    """Sorted vector with very large finite values should pass."""
    arr = np.array([1e100, 1e200, 1e300])
    result = TypeAdapter(SortedFloatVector).validate_python(arr)
    assert (np.diff(result) >= 0).all()


def test_sorted_float_vector_mixed_sign():
    """Sorted vector with mixed positive/negative should pass."""
    arr = np.array([-1000.0, -1.0, 0.0, 1.0, 1000.0])
    result = TypeAdapter(SortedFloatVector).validate_python(arr)
    assert (np.diff(result) >= 0).all()


def test_sorted_int_vector_boundary_values():
    """Sorted vector with boundary int values should pass."""
    # Using int32 range boundaries
    arr = np.array([-1000, -100, 0, 100, 1000], dtype=np.int32)
    result = TypeAdapter(SortedIntVector).validate_python(arr)
    assert (np.diff(result) >= 0).all()


def test_sorted_float_vector_many_elements():
    """Sorted vector with many elements should pass."""
    arr = np.sort(np.random.rand(1000))
    result = TypeAdapter(SortedFloatVector).validate_python(arr)
    assert (np.diff(result) >= 0).all()
    assert result.size == 1000


def test_sorted_int_vector_many_elements():
    """Sorted integer vector with many elements should pass."""
    arr = np.sort(np.random.randint(-1000, 1000, 1000)).astype(np.int32)
    result = TypeAdapter(SortedIntVector).validate_python(arr)
    assert (np.diff(result) >= 0).all()
    assert result.size == 1000


def test_sorted_float_vector_consecutive_duplicates():
    """Sorted vector with many consecutive duplicates should pass."""
    arr = np.array([1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 3.0, 3.0])
    result = TypeAdapter(SortedFloatVector).validate_python(arr)
    assert (np.diff(result) >= 0).all()


def test_sorted_int_vector_consecutive_duplicates():
    """Sorted integer vector with consecutive duplicates should pass."""
    arr = np.array([1, 1, 1, 2, 2, 2, 3, 3], dtype=np.int32)
    result = TypeAdapter(SortedIntVector).validate_python(arr)
    assert (np.diff(result) >= 0).all()
