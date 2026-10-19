"""Test FittableArray_ type validation using pydantic validate_call."""

import numpy as np
import pytest
from pydantic import TypeAdapter, ValidationError, validate_call
from pydantic_core import PydanticCustomError

from quasar_typing.numpy import (
    FittableFloatArray,
    FittableFloatCube,
    FittableFloatMatrix,
    FittableFloatVector,
)

# ============================================================================
# FittableFloatArray Tests
# ============================================================================

def test_fittable_float_array_valid(float_1d_basic):
    """Valid fittable array with finite values should pass."""
    result = TypeAdapter(FittableFloatArray).validate_python(float_1d_basic)
    assert isinstance(result, np.ndarray)


def test_fittable_float_array_valid_2d(float_2d_basic):
    """Valid 2D fittable array should pass validation."""
    result = TypeAdapter(FittableFloatArray).validate_python(float_2d_basic)
    assert result.ndim == 2


def test_fittable_float_array_valid_3d(float_3d_basic):
    """Valid 3D fittable array should pass validation."""
    result = TypeAdapter(FittableFloatArray).validate_python(float_3d_basic)
    assert result.ndim == 3


def test_fittable_float_array_valid_negative(float_1d_negative):
    """Negative values should pass as long as they're finite."""
    result = TypeAdapter(FittableFloatArray).validate_python(float_1d_negative)
    assert isinstance(result, np.ndarray)


def test_fittable_float_array_valid_zero_values():
    """Zero values should pass."""
    arr = np.array([0.0, 0.0, 0.0])
    result = TypeAdapter(FittableFloatArray).validate_python(arr)
    np.testing.assert_array_equal(result, arr)


def test_fittable_float_array_valid_very_large():
    """Very large but finite values should pass."""
    arr = np.array([1e100, 1e200, 1e300])
    result = TypeAdapter(FittableFloatArray).validate_python(arr)
    assert isinstance(result, np.ndarray)


def test_fittable_float_array_valid_very_small():
    """Very small but finite values should pass."""
    arr = np.array([1e-100, 1e-200, 1e-300])
    result = TypeAdapter(FittableFloatArray).validate_python(arr)
    assert isinstance(result, np.ndarray)


def test_fittable_float_array_valid_mixed_signs():
    """Mixed positive and negative finite values should pass."""
    arr = np.array([-1e10, -1.5, 0.0, 2.3, 1e10])
    result = TypeAdapter(FittableFloatArray).validate_python(arr)
    assert isinstance(result, np.ndarray)


def test_fittable_float_array_invalid_empty():
    """Empty array should raise error."""
    arr = np.array([])
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(FittableFloatArray).validate_python(arr)


def test_fittable_float_array_invalid_nan():
    """Array with NaN should raise error."""
    arr = np.array([1.0, np.nan, 3.0])
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(FittableFloatArray).validate_python(arr)


def test_fittable_float_array_invalid_all_nan():
    """Array with all NaN should raise error."""
    arr = np.array([np.nan, np.nan, np.nan])
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(FittableFloatArray).validate_python(arr)


def test_fittable_float_array_invalid_inf():
    """Array with positive Inf should raise error."""
    arr = np.array([1.0, np.inf, 3.0])
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(FittableFloatArray).validate_python(arr)


def test_fittable_float_array_invalid_neg_inf():
    """Array with negative Inf should raise error."""
    arr = np.array([1.0, -np.inf, 3.0])
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(FittableFloatArray).validate_python(arr)


def test_fittable_float_array_invalid_all_inf():
    """Array with all Inf should raise error."""
    arr = np.array([np.inf, np.inf, np.inf])
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(FittableFloatArray).validate_python(arr)


def test_fittable_float_array_invalid_mixed_inf_nan():
    """Array with both Inf and NaN should raise error."""
    arr = np.array([np.inf, np.nan, 1.0])
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(FittableFloatArray).validate_python(arr)


# ============================================================================
# FittableFloatVector Tests
# ============================================================================

def test_fittable_float_vector_valid_1d(float_1d_basic):
    """Valid 1D fittable array should pass."""
    result = TypeAdapter(FittableFloatVector).validate_python(float_1d_basic)
    assert result.ndim == 1


def test_fittable_float_vector_valid_single_element(float_1d_single):
    """Single-element fittable vector should pass."""
    result = TypeAdapter(FittableFloatVector).validate_python(float_1d_single)
    assert result.size == 1


def test_fittable_float_vector_valid_large():
    """Large fittable vector should pass."""
    arr = np.random.rand(1000).astype(np.float64)
    result = TypeAdapter(FittableFloatVector).validate_python(arr)
    assert result.ndim == 1
    assert result.size == 1000


def test_fittable_float_vector_invalid_empty():
    """Empty fittable vector should raise error."""
    arr = np.array([])
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(FittableFloatVector).validate_python(arr)


def test_fittable_float_vector_invalid_2d():
    """2D array should not be accepted as FittableFloatVector."""
    arr = np.array([[1.0, 2.0], [3.0, 4.0]])
    with pytest.raises(ValidationError):
        TypeAdapter(FittableFloatVector).validate_python(arr)


def test_fittable_float_vector_invalid_nan():
    """FittableFloatVector with NaN should raise error."""
    arr = np.array([1.0, 2.0, np.nan])
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(FittableFloatVector).validate_python(arr)


def test_fittable_float_vector_invalid_inf():
    """FittableFloatVector with Inf should raise error."""
    arr = np.array([1.0, 2.0, np.inf])
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(FittableFloatVector).validate_python(arr)


# ============================================================================
# FittableFloatMatrix Tests
# ============================================================================

def test_fittable_float_matrix_valid_2d(float_2d_basic):
    """Valid 2D fittable array should pass."""
    result = TypeAdapter(FittableFloatMatrix).validate_python(float_2d_basic)
    assert result.ndim == 2


def test_fittable_float_matrix_valid_rectangular(float_2d_rectangular):
    """Rectangular 2D fittable array should pass."""
    result = TypeAdapter(FittableFloatMatrix).validate_python(float_2d_rectangular)
    assert result.ndim == 2
    assert result.shape == (2, 3)


def test_fittable_float_matrix_valid_single_row():
    """2D array with single row should pass."""
    arr = np.array([[1.0, 2.0, 3.0]])
    result = TypeAdapter(FittableFloatMatrix).validate_python(arr)
    assert result.ndim == 2
    assert result.shape == (1, 3)


def test_fittable_float_matrix_valid_single_column():
    """2D array with single column should pass."""
    arr = np.array([[1.0], [2.0], [3.0]])
    result = TypeAdapter(FittableFloatMatrix).validate_python(arr)
    assert result.ndim == 2
    assert result.shape == (3, 1)


def test_fittable_float_matrix_invalid_empty():
    """Empty matrix should raise error."""
    arr = np.zeros((0, 0))
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(FittableFloatMatrix).validate_python(arr)


def test_fittable_float_matrix_invalid_1d():
    """1D array should not be accepted as FittableFloatMatrix."""
    arr = np.array([1.0, 2.0, 3.0])
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(FittableFloatMatrix).validate_python(arr)


def test_fittable_float_matrix_invalid_3d():
    """3D array should not be accepted as FittableFloatMatrix."""
    arr = np.ones((2, 3, 4))
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(FittableFloatMatrix).validate_python(arr)


def test_fittable_float_matrix_invalid_nan():
    """Matrix with NaN should raise error."""
    arr = np.array([[1.0, 2.0], [np.nan, 4.0]])
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(FittableFloatMatrix).validate_python(arr)


def test_fittable_float_matrix_invalid_inf():
    """Matrix with Inf should raise error."""
    arr = np.array([[1.0, np.inf], [3.0, 4.0]])
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(FittableFloatMatrix).validate_python(arr)


# ============================================================================
# FittableFloatCube Tests
# ============================================================================

def test_fittable_float_cube_valid_3d(float_3d_basic):
    """Valid 3D fittable array should pass."""
    result = TypeAdapter(FittableFloatCube).validate_python(float_3d_basic)
    assert result.ndim == 3


def test_fittable_float_cube_valid_single_element(float_3d_single_element):
    """3D array with single element should pass."""
    result = TypeAdapter(FittableFloatCube).validate_python(float_3d_single_element)
    assert result.ndim == 3
    assert result.size == 1


def test_fittable_float_cube_valid_various_shapes():
    """Various 3D shapes should pass."""
    for shape in [(2, 3, 4), (5, 5, 5), (1, 10, 10)]:
        arr = np.ones(shape, dtype=np.float64)
        result = TypeAdapter(FittableFloatCube).validate_python(arr)
        assert result.ndim == 3
        assert result.shape == shape


def test_fittable_float_cube_invalid_empty():
    """Empty 3D array should raise error."""
    arr = np.zeros((0, 0, 0))
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(FittableFloatCube).validate_python(arr)


def test_fittable_float_cube_invalid_1d():
    """1D array should not be accepted as FittableFloatCube."""
    arr = np.array([1.0, 2.0, 3.0])
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(FittableFloatCube).validate_python(arr)


def test_fittable_float_cube_invalid_2d():
    """2D array should not be accepted as FittableFloatCube."""
    arr = np.ones((3, 4))
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(FittableFloatCube).validate_python(arr)


def test_fittable_float_cube_invalid_4d():
    """4D array should not be accepted as FittableFloatCube."""
    arr = np.ones((2, 3, 4, 5))
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(FittableFloatCube).validate_python(arr)


def test_fittable_float_cube_invalid_nan():
    """Cube with NaN should raise error."""
    arr = np.ones((2, 3, 4))
    arr[1, 1, 1] = np.nan
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(FittableFloatCube).validate_python(arr)


def test_fittable_float_cube_invalid_inf():
    """Cube with Inf should raise error."""
    arr = np.ones((2, 3, 4))
    arr[0, 0, 0] = np.inf
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        TypeAdapter(FittableFloatCube).validate_python(arr)


# ============================================================================
# Pydantic validate_call Tests
# ============================================================================

def test_validate_call_with_fittable_vector():
    """Test validate_call with FittableFloatVector type hint."""
    @validate_call
    def sum_values(vec: FittableFloatVector) -> float:
        return float(vec.sum())
    
    arr = np.array([1.0, 2.0, 3.0])
    result = sum_values(arr)
    assert result == 6.0


def test_validate_call_rejects_empty_vector():
    """validate_call should reject empty array for FittableFloatVector."""
    @validate_call
    def sum_values(vec: FittableFloatVector) -> float:
        return float(vec.sum())
    
    with pytest.raises((ValidationError, PydanticCustomError)):
        sum_values(np.array([]))


def test_validate_call_rejects_nan_vector():
    """validate_call should reject NaN for FittableFloatVector."""
    @validate_call
    def sum_values(vec: FittableFloatVector) -> float:
        return float(vec.sum())
    
    with pytest.raises((ValidationError, PydanticCustomError)):
        sum_values(np.array([1.0, np.nan, 3.0]))


def test_validate_call_rejects_inf_vector():
    """validate_call should reject Inf for FittableFloatVector."""
    @validate_call
    def sum_values(vec: FittableFloatVector) -> float:
        return float(vec.sum())
    
    with pytest.raises((ValidationError, PydanticCustomError)):
        sum_values(np.array([1.0, np.inf, 3.0]))


def test_validate_call_with_fittable_matrix():
    """Test validate_call with FittableFloatMatrix type hint."""
    @validate_call
    def matrix_sum(mat: FittableFloatMatrix) -> float:
        return float(mat.sum())
    
    arr = np.array([[1.0, 2.0], [3.0, 4.0]])
    result = matrix_sum(arr)
    assert result == 10.0


def test_validate_call_rejects_empty_matrix():
    """validate_call should reject empty matrix for FittableFloatMatrix."""
    @validate_call
    def matrix_sum(mat: FittableFloatMatrix) -> float:
        return float(mat.sum())
    
    with pytest.raises((ValidationError, PydanticCustomError)):
        matrix_sum(np.zeros((0, 0)))


def test_validate_call_with_fittable_cube():
    """Test validate_call with FittableFloatCube type hint."""
    @validate_call
    def cube_sum(cube: FittableFloatCube) -> float:
        return float(cube.sum())
    
    arr = np.arange(24, dtype=np.float64).reshape(2, 3, 4)
    result = cube_sum(arr)
    assert result == float(np.sum(np.arange(24)))


def test_validate_call_rejects_empty_cube():
    """validate_call should reject empty cube for FittableFloatCube."""
    @validate_call
    def cube_sum(cube: FittableFloatCube) -> float:
        return float(cube.sum())
    
    with pytest.raises((ValidationError, PydanticCustomError)):
        cube_sum(np.zeros((0, 0, 0)))


def test_validate_call_multiple_fittable_params():
    """validate_call should work with multiple fittable parameters."""
    @validate_call
    def combine_vectors(v1: FittableFloatVector, v2: FittableFloatVector) -> float:
        return float((v1 + v2).sum())
    
    arr1 = np.array([1.0, 2.0, 3.0])
    arr2 = np.array([4.0, 5.0, 6.0])
    
    result = combine_vectors(arr1, arr2)
    assert result == 21.0


def test_validate_call_rejects_if_any_param_invalid():
    """validate_call should reject if any parameter is invalid."""
    @validate_call
    def combine_vectors(v1: FittableFloatVector, v2: FittableFloatVector) -> float:
        return float((v1 + v2).sum())
    
    arr1 = np.array([1.0, 2.0, 3.0])
    arr2 = np.array([4.0, np.nan, 6.0])
    
    with pytest.raises((ValidationError, PydanticCustomError)):
        combine_vectors(arr1, arr2)


# ============================================================================
# Type Validation Edge Cases
# ============================================================================

def test_fittable_float_array_boundary_finiteness():
    """Test boundary values for finiteness check."""
    # Maximum finite float
    arr = np.array([1.7976931348623157e+308, 1.0, 2.0])
    result = TypeAdapter(FittableFloatArray).validate_python(arr)
    assert isinstance(result, np.ndarray)


def test_fittable_float_vector_denormalized_numbers():
    """Denormalized (very small) numbers should pass as finite."""
    arr = np.array([2.2250738585072014e-308, 1e-400, 1e-320])
    result = TypeAdapter(FittableFloatVector).validate_python(arr)
    assert isinstance(result, np.ndarray)


def test_fittable_float_matrix_single_value():
    """Single value matrix should pass."""
    arr = np.array([[42.0]])
    result = TypeAdapter(FittableFloatMatrix).validate_python(arr)
    assert result.ndim == 2
    assert result.shape == (1, 1)


def test_fittable_float_cube_single_value():
    """Single value cube should pass."""
    arr = np.array([[[42.0]]])
    result = TypeAdapter(FittableFloatCube).validate_python(arr)
    assert result.ndim == 3
    assert result.shape == (1, 1, 1)
