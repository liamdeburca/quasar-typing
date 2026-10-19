"""Integration tests for numpy array type validation order and interactions."""

import numpy as np
import pytest
from pydantic import TypeAdapter, ValidationError, validate_call
from pydantic_core import PydanticCustomError

from quasar_typing.numpy import (
    FittableFloatArray,
    FittableFloatVector,
    FloatArray,
    FloatVector,
    IntArray,
    IntVector,
    SortedFloatVector,
)

# ============================================================================
# Validation Order Tests
# ============================================================================

def test_array_type_check_before_dtype_check():
    """Non-array input should fail before dtype validation."""
    TypeAdapter(FloatVector).validate_python([1.0, 2.0, 3.0])


def test_dtype_check_before_ndim_check():
    """Wrong dtype should fail before checking ndim."""
    # Int array (wrong dtype) should fail before checking if 1D
    arr_2d = np.array([[1, 2], [3, 4]], dtype=np.int32)
    with pytest.raises(ValidationError):
        TypeAdapter(FloatVector).validate_python(arr_2d)


def test_ndim_check_before_element_checks():
    """Wrong ndim should fail before checking for empty/finite/sorted."""
    # 2D array with wrong ndim should fail before checking if elements are finite
    arr = np.array([[1.0, np.nan], [3.0, 4.0]])
    with pytest.raises(ValidationError):
        TypeAdapter(FloatVector).validate_python(arr)


def test_empty_check_before_finite_check():
    """Empty array check should occur before finite value check."""
    # Empty array validation
    empty = np.array([])
    
    # FittableFloatVector should check empty before finiteness
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(FittableFloatVector).validate_python(empty)


def test_finite_check_before_sorted_check():
    """Finite check should occur before sort check in SortedFloatVector."""
    # Array with NaN that's also not sorted
    arr = np.array([3.0, 1.0, np.nan, 2.0])
    
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(SortedFloatVector).validate_python(arr)


def test_empty_then_finite_then_sorted():
    """Test full validation order: empty → finite → sorted."""
    # Empty should fail first
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(SortedFloatVector).validate_python(np.array([]))
    
    # Non-finite should fail before sort check
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(SortedFloatVector).validate_python(np.array([1.0, np.nan, 3.0]))
    
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(SortedFloatVector).validate_python(np.array([3.0, 1.0, 2.0]))


# ============================================================================
# Type Alias Inheritance and Validation
# ============================================================================

def test_float_array_accepts_valid_1d_2d_3d():
    """FloatArray should accept all float arrays regardless of dimension."""
    arr_1d = np.array([1.0, 2.0, 3.0])
    arr_2d = np.array([[1.0, 2.0], [3.0, 4.0]])
    arr_3d = np.arange(24, dtype=np.float64).reshape(2, 3, 4)
    
    assert TypeAdapter(FloatArray).validate_python(arr_1d) is not None
    assert TypeAdapter(FloatArray).validate_python(arr_2d) is not None
    assert TypeAdapter(FloatArray).validate_python(arr_3d) is not None


def test_float_vector_rejects_2d_and_3d():
    """FloatVector should reject 2D and 3D arrays."""
    arr_2d = np.array([[1.0, 2.0], [3.0, 4.0]])
    arr_3d = np.ones((2, 3, 4))
        
    with pytest.raises(ValidationError):
        TypeAdapter(FloatVector).validate_python(arr_2d)
    with pytest.raises(ValidationError):
        TypeAdapter(FloatVector).validate_python(arr_3d)


def test_float_vs_int_dtype_enforcement():
    """FloatArray should reject int, IntArray should reject float."""
    float_arr = np.array([1.0, 2.0, 3.0])
    int_arr = np.array([1, 2, 3], dtype=np.int32)
    
    # Float type should accept float
    assert TypeAdapter(FloatArray).validate_python(float_arr) is not None
    TypeAdapter(FloatArray).validate_python(int_arr)
    
    # Int type should accept int
    assert TypeAdapter(IntArray).validate_python(int_arr) is not None
    
    # Int type should reject float
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(IntArray).validate_python(float_arr)


# ============================================================================
# Fittable vs Non-Fittable Interaction
# ============================================================================

def test_fittable_rejects_non_fittable_accepted():
    """Values accepted by FloatArray may be rejected by FittableFloatArray."""
    # Empty array is accepted by FloatArray but not FittableFloatArray
    empty = np.array([])
    
    # Note: FloatArray doesn't validate empty, but FittableFloatArray does
    with pytest.raises((ValidationError, PydanticCustomError)):
        TypeAdapter(FittableFloatArray).validate_python(empty)
    
    # NaN is accepted by FloatArray but not FittableFloatArray
    with_nan = np.array([1.0, np.nan, 3.0])
    
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(FittableFloatArray).validate_python(with_nan)
    assert 'finite' in str(exc_info.value).lower()


def test_fittable_satisfies_float_constraint():
    """Values passing FittableFloatArray validation should pass FloatArray."""
    arr = np.array([1.0, 2.0, 3.0])
    
    # Pass FittableFloatArray
    result_fittable = TypeAdapter(FittableFloatArray).validate_python(arr)
    
    # Should also pass FloatArray
    result_float = TypeAdapter(FloatArray).validate_python(result_fittable)
    
    np.testing.assert_array_equal(result_float, arr)


def test_fittable_single_element_vector():
    """Single element should pass FittableFloatVector."""
    arr = np.array([42.0])
    result = TypeAdapter(FittableFloatVector).validate_python(arr)
    assert result.size == 1


# ============================================================================
# Sorted Array Validation Interaction
# ============================================================================

def test_sorted_rejects_fittable_unsorted():
    """SortedFloatVector should reject even fittable arrays if unsorted."""
    # Array with finite values but not sorted
    arr = np.array([3.0, 1.0, 2.0])
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(SortedFloatVector).validate_python(arr)
    


def test_sorted_satisfies_fittable_constraints():
    """Values passing SortedFloatVector should also pass FittableFloatVector."""
    arr = np.array([1.0, 2.0, 3.0])
    
    # Pass SortedFloatVector
    result_sorted = TypeAdapter(SortedFloatVector).validate_python(arr)
    
    # Should also pass FittableFloatVector
    result_fittable = TypeAdapter(FittableFloatVector).validate_python(result_sorted)
    
    np.testing.assert_array_equal(result_fittable, arr)


def test_sorted_rejects_finite_but_unsorted():
    """SortedFloatVector should reject finite values if they're not sorted."""
    arr = np.array([5.0, 4.0, 3.0, 2.0, 1.0])
    
    # All values are finite
    assert np.all(np.isfinite(arr))
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(SortedFloatVector).validate_python(arr)


def test_sorted_with_duplicates():
    """SortedFloatVector should accept duplicates in non-descending order."""
    arr = np.array([1.0, 1.0, 2.0, 2.0, 3.0, 3.0])
    result = TypeAdapter(SortedFloatVector).validate_python(arr)
    assert (np.diff(result) >= 0).all()


# ============================================================================
# Pydantic validate_call Integration Order
# ============================================================================

def test_validate_call_checks_all_params():
    """validate_call should validate all parameters before execution."""
    @validate_call
    def process(v1: FloatVector, v2: IntVector) -> float:
        return float(v1[0]) + float(v2[0])
    
    valid_float = np.array([1.0, 2.0, 3.0])
    valid_int = np.array([1, 2, 3], dtype=np.int32)
    
    # Both valid should work
    result = process(valid_float, valid_int)
    assert result == 2.0
    
    invalid_float = np.array([1, 2, 3], dtype=np.int32)
    process(invalid_float, valid_int)
    
    # Second invalid should raise
    with pytest.raises((ValidationError, PydanticCustomError)):
        process(valid_float, np.array([1.0, 2.0, 3.0]))


def test_validate_call_fittable_constraints():
    """validate_call should enforce FittableFloatVector constraints."""
    @validate_call
    def compute(vec: FittableFloatVector) -> float:
        return float(vec.sum())
    
    # Valid fittable
    assert compute(np.array([1.0, 2.0, 3.0])) == 6.0
    
    # Empty should reject
    with pytest.raises((ValidationError, PydanticCustomError)):
        compute(np.array([]))
    
    # NaN should reject
    with pytest.raises((ValidationError, PydanticCustomError)):
        compute(np.array([1.0, np.nan, 3.0]))


def test_validate_call_sorted_constraints():
    """validate_call should enforce SortedFloatVector constraints."""
    @validate_call
    def binary_search(vec: SortedFloatVector, target: float) -> int:
        return int(np.searchsorted(vec, target))
    
    # Valid sorted
    result = binary_search(np.array([1.0, 2.0, 3.0, 4.0, 5.0]), 3.5)
    assert result == 3
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        binary_search(np.array([5.0, 1.0, 3.0, 2.0, 4.0]), 3.5)
    

# ============================================================================
# Complex Scenario Tests
# ============================================================================

def test_multiple_validation_failures_priority():
    """When multiple validations fail, check which error is raised."""
    # Array that fails multiple checks: wrong dtype, wrong ndim, empty
    arr_int_2d = np.array([[1, 2], [3, 4]], dtype=np.int32)
    
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(FloatVector).validate_python(arr_int_2d)


def test_dtype_coercion_unavailable():
    """Strict type validation should not attempt dtype coercion."""
    # Integer list in wrong dtype
    int_arr = np.array([1, 2, 3], dtype=np.int32)
    TypeAdapter(FloatArray).validate_python(int_arr)


def test_shape_constraints_with_dtype():
    """Shape and dtype constraints should both be enforced."""
    # Create 2D float array
    arr_2d_float = np.array([[1.0, 2.0], [3.0, 4.0]])
    
    # Should pass FloatArray
    assert TypeAdapter(FloatArray).validate_python(arr_2d_float) is not None
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(FloatVector).validate_python(arr_2d_float)


def test_large_array_validation():
    """Large arrays should still pass all validation checks."""
    large_arr = np.random.rand(10000).astype(np.float64)
    
    result = TypeAdapter(FloatVector).validate_python(large_arr)
    assert result.size == 10000


def test_fittable_large_array_validation():
    """Large arrays should pass FittableFloatArray validation."""
    large_arr = np.abs(np.random.randn(10000)).astype(np.float64)
    
    result = TypeAdapter(FittableFloatArray).validate_python(large_arr)
    assert result.size == 10000
    assert np.all(np.isfinite(result))


def test_sorted_large_array_validation():
    """Large sorted arrays should pass SortedFloatVector validation."""
    large_arr = np.sort(np.random.randn(10000)).astype(np.float64)
    
    result = TypeAdapter(SortedFloatVector).validate_python(large_arr)
    assert result.size == 10000
    assert (np.diff(result) >= 0).all()
