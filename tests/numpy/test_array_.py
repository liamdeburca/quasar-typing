"""Test Array_ class and type aliases using pydantic TypeAdapter."""

import numpy as np
import pytest
from pydantic import TypeAdapter, validate_call
from pydantic_core import PydanticCustomError, ValidationError

from quasar_typing.numpy import (
    BoolArray,
    BoolCube,
    BoolMatrix,
    BoolVector,
    FittableFloatArray,
    FittableFloatCube,
    FittableFloatMatrix,
    FittableFloatVector,
    FloatArray,
    FloatCube,
    FloatMatrix,
    FloatVector,
    IntArray,
    IntCube,
    IntMatrix,
    IntVector,
    SortedFloatVector,
    SortedIntVector,
)

# ============================================================================
# FloatArray Tests
# ============================================================================

def test_float_array_valid_1d(float_1d_basic):
    """Valid 1D float array should pass validation."""
    adapter = TypeAdapter(FloatArray)
    result = adapter.validate_python(float_1d_basic)
    assert isinstance(result, np.ndarray)
    assert result.dtype in [np.float64, np.floating]


def test_float_array_valid_2d(float_2d_basic):
    """Valid 2D float array should pass validation."""
    adapter = TypeAdapter(FloatArray)
    result = adapter.validate_python(float_2d_basic)
    assert isinstance(result, np.ndarray)
    assert result.ndim == 2


def test_float_array_valid_3d(float_3d_basic):
    """Valid 3D float array should pass validation."""
    adapter = TypeAdapter(FloatArray)
    result = adapter.validate_python(float_3d_basic)
    assert isinstance(result, np.ndarray)
    assert result.ndim == 3


def test_float_array_accepts_list():
    """FloatArray should coerce Python list to array."""
    adapter = TypeAdapter(FloatArray)
    result = adapter.validate_python([1.0, 2.0, 3.0])
    assert isinstance(result, np.ndarray)
    assert result.dtype == np.float64


def test_float_array_accepts_tuple():
    """FloatArray should coerce tuple to array."""
    adapter = TypeAdapter(FloatArray)
    result = adapter.validate_python((1.0, 2.0, 3.0))
    assert isinstance(result, np.ndarray)
    assert result.dtype == np.float64


def test_float_array_accepts_scalar():
    """FloatArray should coerce scalar value to 0-d array."""
    adapter = TypeAdapter(FloatArray)
    result = adapter.validate_python(42.0)
    assert isinstance(result, np.ndarray)
    assert result.dtype == np.float64


def test_float_array_rejects_string():
    """FloatArray should reject string."""
    adapter = TypeAdapter(FloatArray)
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python("not an array")


def test_float_array_rejects_dict():
    """FloatArray should reject dictionary."""
    adapter = TypeAdapter(FloatArray)
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python({"a": 1.0})


def test_float_array_accepts_int_array():
    """FloatArray should coerce integer array to float."""
    adapter = TypeAdapter(FloatArray)
    arr = np.array([1, 2, 3], dtype=np.int32)
    result = adapter.validate_python(arr)
    assert result.dtype == np.float64


def test_float_array_accepts_float32(float32_array):
    """FloatArray should coerce float32 to float64."""
    adapter = TypeAdapter(FloatArray)
    result = adapter.validate_python(float32_array)
    assert result.dtype == np.float64


def test_float_array_accepts_float64(float64_array):
    """FloatArray should accept float64."""
    adapter = TypeAdapter(FloatArray)
    result = adapter.validate_python(float64_array)
    assert result.dtype in [np.float64, np.floating]


# ============================================================================
# FloatVector Tests
# ============================================================================

def test_float_vector_valid_1d(float_1d_basic):
    """Valid 1D float array should pass FloatVector validation."""
    adapter = TypeAdapter(FloatVector)
    result = adapter.validate_python(float_1d_basic)
    assert result.ndim == 1


def test_float_vector_valid_single_element(float_1d_single):
    """Single-element 1D float array should pass."""
    adapter = TypeAdapter(FloatVector)
    result = adapter.validate_python(float_1d_single)
    assert result.size == 1


def test_float_vector_valid_large(float_1d_large):
    """Large 1D float array should pass."""
    adapter = TypeAdapter(FloatVector)
    result = adapter.validate_python(float_1d_large)
    assert result.ndim == 1
    assert result.size == 100


# ============================================================================
# FloatMatrix Tests
# ============================================================================

def test_float_matrix_valid_2d(float_2d_basic):
    """Valid 2D float array should pass FloatMatrix validation."""
    adapter = TypeAdapter(FloatMatrix)
    result = adapter.validate_python(float_2d_basic)
    assert result.ndim == 2


def test_float_matrix_valid_rectangular(float_2d_rectangular):
    """Rectangular 2D float array should pass."""
    adapter = TypeAdapter(FloatMatrix)
    result = adapter.validate_python(float_2d_rectangular)
    assert result.ndim == 2
    assert result.shape == (2, 3)


def test_float_matrix_rejects_1d():
    """FloatMatrix should reject 1D array (reshape coercion fails)."""
    adapter = TypeAdapter(FloatMatrix)
    arr = np.array([1.0, 2.0, 3.0])
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python(arr)


def test_float_matrix_rejects_3d():
    """FloatMatrix should reject 3D array (reshape coercion fails)."""
    adapter = TypeAdapter(FloatMatrix)
    arr = np.arange(24, dtype=np.float64).reshape(2, 3, 4)
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python(arr)


# ============================================================================
# FloatCube Tests
# ============================================================================

def test_float_cube_valid_3d(float_3d_basic):
    """Valid 3D float array should pass FloatCube validation."""
    adapter = TypeAdapter(FloatCube)
    result = adapter.validate_python(float_3d_basic)
    assert result.ndim == 3


def test_float_cube_valid_single_element(float_3d_single_element):
    """3D array with single element should pass."""
    adapter = TypeAdapter(FloatCube)
    result = adapter.validate_python(float_3d_single_element)
    assert result.ndim == 3
    assert result.size == 1


def test_float_cube_rejects_1d():
    """FloatCube should reject 1D array (reshape coercion fails)."""
    adapter = TypeAdapter(FloatCube)
    arr = np.array([1.0, 2.0, 3.0])
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python(arr)


def test_float_cube_rejects_2d():
    """FloatCube should reject 2D array (reshape coercion fails)."""
    adapter = TypeAdapter(FloatCube)
    arr = np.array([[1.0, 2.0], [3.0, 4.0]])
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python(arr)


# ============================================================================
# IntArray Tests
# ============================================================================

def test_int_array_valid_1d(int_1d_basic):
    """Valid 1D integer array should pass validation."""
    adapter = TypeAdapter(IntArray)
    result = adapter.validate_python(int_1d_basic)
    assert isinstance(result, np.ndarray)
    assert result.dtype == np.int64


def test_int_array_valid_2d(int_2d_basic):
    """Valid 2D integer array should pass validation."""
    adapter = TypeAdapter(IntArray)
    result = adapter.validate_python(int_2d_basic)
    assert result.ndim == 2


def test_int_array_valid_3d(int_3d_basic):
    """Valid 3D integer array should pass validation."""
    adapter = TypeAdapter(IntArray)
    result = adapter.validate_python(int_3d_basic)
    assert result.ndim == 3


def test_int_array_accepts_float_array():
    """IntArray cannot coerce float to int."""
    adapter = TypeAdapter(IntArray)
    arr = np.array([1.0, 2.0, 3.0])
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python(arr)

# ============================================================================
# IntVector Tests
# ============================================================================

def test_int_vector_valid_1d(int_1d_basic):
    """Valid 1D integer array should pass IntVector validation."""
    adapter = TypeAdapter(IntVector)
    result = adapter.validate_python(int_1d_basic)
    assert result.ndim == 1


def test_int_vector_valid_single_element(int_1d_single):
    """Single-element 1D integer array should pass."""
    adapter = TypeAdapter(IntVector)
    result = adapter.validate_python(int_1d_single)
    assert result.size == 1


# ============================================================================
# IntMatrix Tests
# ============================================================================

def test_int_matrix_valid_2d(int_2d_basic):
    """Valid 2D integer array should pass IntMatrix validation."""
    adapter = TypeAdapter(IntMatrix)
    result = adapter.validate_python(int_2d_basic)
    assert result.ndim == 2


def test_int_matrix_rejects_1d():
    """IntMatrix should reject 1D array (reshape coercion fails)."""
    adapter = TypeAdapter(IntMatrix)
    arr = np.array([1, 2, 3], dtype=np.int32)
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python(arr)


# ============================================================================
# IntCube Tests
# ============================================================================

def test_int_cube_valid_3d(int_3d_basic):
    """Valid 3D integer array should pass IntCube validation."""
    adapter = TypeAdapter(IntCube)
    result = adapter.validate_python(int_3d_basic)
    assert result.ndim == 3


def test_int_cube_rejects_1d():
    """IntCube should reject 1D array (reshape coercion fails)."""
    adapter = TypeAdapter(IntCube)
    arr = np.array([1, 2, 3], dtype=np.int32)
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python(arr)


# ============================================================================
# BoolArray Tests
# ============================================================================

def test_bool_array_valid_1d(bool_1d_basic):
    """Valid 1D boolean array should pass validation."""
    adapter = TypeAdapter(BoolArray)
    result = adapter.validate_python(bool_1d_basic)
    assert result.dtype == bool


def test_bool_array_valid_2d(bool_2d_basic):
    """Valid 2D boolean array should pass validation."""
    adapter = TypeAdapter(BoolArray)
    result = adapter.validate_python(bool_2d_basic)
    assert result.ndim == 2


def test_bool_array_valid_3d(bool_3d_basic):
    """Valid 3D boolean array should pass validation."""
    adapter = TypeAdapter(BoolArray)
    result = adapter.validate_python(bool_3d_basic)
    assert result.ndim == 3


def test_bool_array_all_true(bool_1d_all_true):
    """Boolean array with all True values should pass."""
    adapter = TypeAdapter(BoolArray)
    result = adapter.validate_python(bool_1d_all_true)
    assert result.all()


def test_bool_array_all_false(bool_1d_all_false):
    """Boolean array with all False values should pass."""
    adapter = TypeAdapter(BoolArray)
    result = adapter.validate_python(bool_1d_all_false)
    assert not result.any()


# ============================================================================
# BoolVector Tests
# ============================================================================

def test_bool_vector_valid_1d(bool_1d_basic):
    """Valid 1D boolean array should pass BoolVector validation."""
    adapter = TypeAdapter(BoolVector)
    result = adapter.validate_python(bool_1d_basic)
    assert result.ndim == 1


# ============================================================================
# BoolMatrix Tests
# ============================================================================

def test_bool_matrix_valid_2d(bool_2d_basic):
    """Valid 2D boolean array should pass BoolMatrix validation."""
    adapter = TypeAdapter(BoolMatrix)
    result = adapter.validate_python(bool_2d_basic)
    assert result.ndim == 2


def test_bool_matrix_rejects_1d():
    """BoolMatrix should reject 1D array (reshape coercion fails)."""
    adapter = TypeAdapter(BoolMatrix)
    arr = np.array([True, False, True])
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python(arr)


# ============================================================================
# BoolCube Tests
# ============================================================================

def test_bool_cube_valid_3d(bool_3d_basic):
    """Valid 3D boolean array should pass BoolCube validation."""
    adapter = TypeAdapter(BoolCube)
    result = adapter.validate_python(bool_3d_basic)
    assert result.ndim == 3


def test_bool_cube_rejects_1d():
    """BoolCube should reject 1D array (reshape coercion fails)."""
    adapter = TypeAdapter(BoolCube)
    arr = np.array([True, False, True])
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python(arr)


# ============================================================================
# Fittable Array Tests
# ============================================================================

def test_fittable_float_array_valid(float_1d_basic):
    """Valid fittable array with finite values should pass."""
    adapter = TypeAdapter(FittableFloatArray)
    result = adapter.validate_python(float_1d_basic)
    assert isinstance(result, np.ndarray)


def test_fittable_float_array_rejects_empty():
    """FittableFloatArray should reject empty array."""
    adapter = TypeAdapter(FittableFloatArray)
    arr = np.array([])
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        adapter.validate_python(arr)
    assert 'at least one element' in str(exc_info.value)


def test_fittable_float_array_rejects_nan():
    """FittableFloatArray should reject array with NaN."""
    adapter = TypeAdapter(FittableFloatArray)
    arr = np.array([1.0, np.nan, 3.0])
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        adapter.validate_python(arr)
    assert 'finite' in str(exc_info.value)


def test_fittable_float_array_rejects_inf():
    """FittableFloatArray should reject array with Inf."""
    adapter = TypeAdapter(FittableFloatArray)
    arr = np.array([1.0, np.inf, 3.0])
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        adapter.validate_python(arr)
    assert 'finite' in str(exc_info.value)


def test_fittable_float_array_rejects_neg_inf():
    """FittableFloatArray should reject array with negative Inf."""
    adapter = TypeAdapter(FittableFloatArray)
    arr = np.array([1.0, -np.inf, 3.0])
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        adapter.validate_python(arr)
    assert 'finite' in str(exc_info.value)


def test_fittable_float_vector_valid_1d(float_1d_basic):
    """Valid 1D fittable array should pass."""
    adapter = TypeAdapter(FittableFloatVector)
    result = adapter.validate_python(float_1d_basic)
    assert result.ndim == 1


def test_fittable_float_vector_rejects_empty():
    """FittableFloatVector should reject empty array."""
    adapter = TypeAdapter(FittableFloatVector)
    arr = np.array([])
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python(arr)


def test_fittable_float_matrix_valid_2d(float_2d_basic):
    """Valid 2D fittable array should pass."""
    adapter = TypeAdapter(FittableFloatMatrix)
    result = adapter.validate_python(float_2d_basic)
    assert result.ndim == 2


def test_fittable_float_matrix_rejects_empty():
    """FittableFloatMatrix should reject empty array."""
    adapter = TypeAdapter(FittableFloatMatrix)
    arr = np.zeros((0, 0))
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python(arr)


def test_fittable_float_cube_valid_3d(float_3d_basic):
    """Valid 3D fittable array should pass."""
    adapter = TypeAdapter(FittableFloatCube)
    result = adapter.validate_python(float_3d_basic)
    assert result.ndim == 3


def test_fittable_float_cube_rejects_empty():
    """FittableFloatCube should reject empty array."""
    adapter = TypeAdapter(FittableFloatCube)
    arr = np.zeros((0, 0, 0))
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python(arr)


# ============================================================================
# Sorted Array Tests
# ============================================================================

def test_sorted_float_vector_valid(sorted_float_1d_basic):
    """Valid sorted 1D float array should pass."""
    adapter = TypeAdapter(SortedFloatVector)
    result = adapter.validate_python(sorted_float_1d_basic)
    assert (np.diff(result) >= 0).all()


def test_sorted_float_vector_with_duplicates(sorted_float_1d_with_duplicates):
    """Sorted array with duplicates should pass."""
    adapter = TypeAdapter(SortedFloatVector)
    result = adapter.validate_python(sorted_float_1d_with_duplicates)
    assert (np.diff(result) >= 0).all()


def test_sorted_float_vector_negative(sorted_float_1d_negative):
    """Sorted array with negative values should pass."""
    adapter = TypeAdapter(SortedFloatVector)
    result = adapter.validate_python(sorted_float_1d_negative)
    assert (np.diff(result) >= 0).all()


def test_sorted_float_vector_rejects_empty():
    """SortedFloatVector should reject empty array."""
    adapter = TypeAdapter(SortedFloatVector)
    arr = np.array([])
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python(arr)


def test_sorted_int_vector_valid(sorted_int_1d_basic):
    """Valid sorted 1D integer array should pass."""
    adapter = TypeAdapter(SortedIntVector)
    result = adapter.validate_python(sorted_int_1d_basic)
    assert (np.diff(result) >= 0).all()


def test_sorted_int_vector_with_duplicates(sorted_int_1d_with_duplicates):
    """Sorted integer array with duplicates should pass."""
    adapter = TypeAdapter(SortedIntVector)
    result = adapter.validate_python(sorted_int_1d_with_duplicates)
    assert (np.diff(result) >= 0).all()


# ============================================================================
# Pydantic validate_call Tests
# ============================================================================

def test_validate_call_with_float_vector():
    """Test validate_call decorator with FloatVector type hint."""
    @validate_call
    def process_vector(vec: FloatVector) -> float:
        return float(vec.sum())
    
    arr = np.array([1.0, 2.0, 3.0])
    result = process_vector(arr)
    assert result == 6.0


def test_validate_call_rejects_wrong_type():
    """validate_call should reject incompatible types."""
    @validate_call
    def process_vector(vec: FloatVector) -> float:
        return float(vec.sum())

    with pytest.raises((ValidationError, PydanticCustomError)):
        process_vector("not an array")


def test_validate_call_with_int_vector():
    """Test validate_call with IntVector type hint."""
    @validate_call
    def process_int_vector(vec: IntVector) -> int:
        return int(vec.sum())
    
    arr = np.array([1, 2, 3], dtype=np.int32)
    result = process_int_vector(arr)
    assert result == 6


def test_validate_call_rejects_empty_fittable():
    """validate_call should reject empty array for FittableFloatVector."""
    @validate_call
    def process_fittable(vec: FittableFloatVector) -> float:
        return float(vec.sum())
    
    with pytest.raises((ValidationError, PydanticCustomError)):
        process_fittable(np.array([]))


def test_validate_call_rejects_nan_fittable():
    """validate_call should reject NaN for FittableFloatVector."""
    @validate_call
    def process_fittable(vec: FittableFloatVector) -> float:
        return float(vec.sum())
    
    with pytest.raises((ValidationError, PydanticCustomError)):
        process_fittable(np.array([1.0, np.nan, 3.0]))


def test_validate_call_with_sorted_vector():
    """Test validate_call with SortedFloatVector type hint."""
    @validate_call
    def process_sorted(vec: SortedFloatVector) -> float:
        return float(vec[-1])
    
    arr = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    result = process_sorted(arr)
    assert result == 5.0


def test_validate_call_rejects_unsorted_with_hint():
    """validate_call should reject unsorted array for SortedFloatVector."""
    @validate_call
    def process_sorted(vec: SortedFloatVector) -> float:
        return float(vec[-1])

    with pytest.raises(ValidationError):
        process_sorted(np.array([1.0, 3.0, 2.0, 4.0]))


def test_validate_call_with_float_matrix():
    """Test validate_call with FloatMatrix type hint."""
    @validate_call
    def process_matrix(mat: FloatMatrix) -> float:
        return float(mat.sum())
    
    arr = np.array([[1.0, 2.0], [3.0, 4.0]])
    result = process_matrix(arr)
    assert result == 10.0


def test_validate_call_with_bool_vector():
    """Test validate_call with BoolVector type hint."""
    @validate_call
    def count_true(vec: BoolVector) -> int:
        return int(vec.sum())
    
    arr = np.array([True, True, False])
    result = count_true(arr)
    assert result == 2


# ============================================================================
# Type Validation with validate_call
# ============================================================================

def test_validate_call_enforces_dtype():
    """validate_call should enforce dtype constraints."""
    @validate_call
    def needs_float_vector(vec: FloatVector) -> None:
        pass
    
    # Integer array should not be accepted as FloatVector
    int_arr = np.array([1, 2, 3], dtype=np.int32)
    needs_float_vector(int_arr)


def test_validate_call_enforces_ndim():
    """validate_call should enforce ndim constraints."""
    @validate_call
    def needs_float_vector(vec: FloatVector) -> None:
        pass
    
    # 2D array should not be accepted as FloatVector
    arr_2d = np.array([[1.0, 2.0], [3.0, 4.0]])
    with pytest.raises(ValidationError):
        needs_float_vector(arr_2d)


def test_validate_call_multiple_parameters():
    """validate_call should work with multiple array parameters."""
    @validate_call
    def add_vectors(v1: FloatVector, v2: FloatVector) -> float:
        return float((v1 + v2).sum())
    
    arr1 = np.array([1.0, 2.0, 3.0])
    arr2 = np.array([4.0, 5.0, 6.0])
    result = add_vectors(arr1, arr2)
    assert result == 21.0
