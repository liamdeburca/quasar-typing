"""Shared test fixtures for numpy submodule tests."""

import numpy as np
import pytest
from numpy.random import RandomState

# ============================================================================
# Float Arrays and Vectors
# ============================================================================

@pytest.fixture
def float_1d_basic():
    """Basic 1D float array."""
    return np.array([1.0, 2.0, 3.0])


@pytest.fixture
def float_1d_single():
    """Single-element 1D float array."""
    return np.array([42.0])


@pytest.fixture
def float_1d_large():
    """Large 1D float array."""
    return np.arange(100, dtype=np.float64)


@pytest.fixture
def float_1d_negative():
    """1D float array with negative values."""
    return np.array([-10.0, -5.0, -1.0, 0.0, 1.0])


@pytest.fixture
def float_1d_with_duplicates():
    """1D float array with duplicate values."""
    return np.array([1.0, 1.0, 2.0, 2.0, 3.0, 3.0])


@pytest.fixture
def float_1d_small_values():
    """1D float array with small but finite values."""
    return np.array([1e-10, 1e-20, 1e-30])


@pytest.fixture
def float_1d_large_values():
    """1D float array with large but finite values."""
    return np.array([1e100, 1e200, 1e300])


@pytest.fixture
def float_2d_basic():
    """Basic 2D float array."""
    return np.array([[1.0, 2.0], [3.0, 4.0]])


@pytest.fixture
def float_2d_rectangular():
    """Rectangular 2D float array (different dimensions)."""
    return np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])


@pytest.fixture
def float_2d_large():
    """Large 2D float array."""
    return np.random.rand(10, 10).astype(np.float64)


@pytest.fixture
def float_3d_basic():
    """Basic 3D float array."""
    return np.arange(24, dtype=np.float64).reshape(2, 3, 4)


@pytest.fixture
def float_3d_single_element():
    """3D array with single element."""
    return np.array([[[1.0]]])


# ============================================================================
# Integer Arrays and Vectors
# ============================================================================

@pytest.fixture
def int_1d_basic():
    """Basic 1D integer array."""
    return np.array([1, 2, 3], dtype=np.int32)


@pytest.fixture
def int_1d_single():
    """Single-element 1D integer array."""
    return np.array([42], dtype=np.int32)


@pytest.fixture
def int_1d_negative():
    """1D integer array with negative values."""
    return np.array([-10, -5, -1, 0, 1], dtype=np.int32)


@pytest.fixture
def int_1d_large():
    """Large 1D integer array."""
    return np.arange(100, dtype=np.int32)


@pytest.fixture
def int_1d_with_duplicates():
    """1D integer array with duplicate values."""
    return np.array([1, 1, 2, 2, 3, 3], dtype=np.int32)


@pytest.fixture
def int_2d_basic():
    """Basic 2D integer array."""
    return np.array([[1, 2], [3, 4]], dtype=np.int32)


@pytest.fixture
def int_2d_rectangular():
    """Rectangular 2D integer array."""
    return np.array([[1, 2, 3], [4, 5, 6]], dtype=np.int32)


@pytest.fixture
def int_3d_basic():
    """Basic 3D integer array."""
    return np.arange(24, dtype=np.int32).reshape(2, 3, 4)


# ============================================================================
# Boolean Arrays and Vectors
# ============================================================================

@pytest.fixture
def bool_1d_basic():
    """Basic 1D boolean array."""
    return np.array([True, False, True])


@pytest.fixture
def bool_1d_all_true():
    """1D boolean array with all True values."""
    return np.array([True, True, True])


@pytest.fixture
def bool_1d_all_false():
    """1D boolean array with all False values."""
    return np.array([False, False, False])


@pytest.fixture
def bool_1d_single():
    """Single-element 1D boolean array."""
    return np.array([True])


@pytest.fixture
def bool_2d_basic():
    """Basic 2D boolean array."""
    return np.array([[True, False], [True, True]])


@pytest.fixture
def bool_3d_basic():
    """Basic 3D boolean array."""
    return np.random.rand(2, 3, 4) > 0.5


# ============================================================================
# Sorted Arrays
# ============================================================================

@pytest.fixture
def sorted_float_1d_basic():
    """Basic sorted 1D float array."""
    return np.array([1.0, 2.0, 3.0, 4.0, 5.0])


@pytest.fixture
def sorted_float_1d_with_duplicates():
    """Sorted 1D float array with duplicate values."""
    return np.array([1.0, 1.0, 2.0, 2.0, 3.0, 3.0])


@pytest.fixture
def sorted_float_1d_negative():
    """Sorted 1D float array with negative values."""
    return np.array([-10.0, -5.0, -1.0, 0.0, 1.0])


@pytest.fixture
def sorted_float_1d_decimal():
    """Sorted 1D float array with decimal values."""
    return np.array([0.1, 0.5, 1.2, 5.3, 10.2])


@pytest.fixture
def sorted_float_1d_single():
    """Single-element sorted 1D float array."""
    return np.array([42.0])


@pytest.fixture
def sorted_int_1d_basic():
    """Basic sorted 1D integer array."""
    return np.array([1, 2, 3, 4, 5], dtype=np.int32)


@pytest.fixture
def sorted_int_1d_with_duplicates():
    """Sorted 1D integer array with duplicate values."""
    return np.array([1, 1, 2, 2, 3, 3], dtype=np.int32)


@pytest.fixture
def sorted_int_1d_negative():
    """Sorted 1D integer array with negative values."""
    return np.array([-10, -5, -1, 0, 1], dtype=np.int32)


# ============================================================================
# Arrays with Special Values (NaN, Inf)
# ============================================================================

@pytest.fixture
def float_1d_with_nan():
    """1D float array with NaN value."""
    return np.array([1.0, np.nan, 3.0])


@pytest.fixture
def float_1d_with_inf():
    """1D float array with Inf value."""
    return np.array([1.0, np.inf, 3.0])


@pytest.fixture
def float_1d_with_neg_inf():
    """1D float array with negative Inf value."""
    return np.array([1.0, -np.inf, 3.0])


@pytest.fixture
def float_1d_all_nan():
    """1D float array with all NaN values."""
    return np.array([np.nan, np.nan, np.nan])


@pytest.fixture
def float_1d_all_inf():
    """1D float array with all Inf values."""
    return np.array([np.inf, np.inf, np.inf])


# ============================================================================
# Coordinate Tuples
# ============================================================================

@pytest.fixture
def coords_float_matching_1d():
    """3-tuple of matching 1D float arrays."""
    arr1 = np.array([1.0, 2.0, 3.0])
    arr2 = np.array([4.0, 5.0, 6.0])
    arr3 = np.array([7.0, 8.0, 9.0])
    return (arr1, arr2, arr3)


@pytest.fixture
def coords_float_matching_2d():
    """3-tuple of matching 2D float arrays."""
    arr1 = np.array([[1.0, 2.0], [3.0, 4.0]])
    arr2 = np.array([[5.0, 6.0], [7.0, 8.0]])
    arr3 = np.array([[9.0, 10.0], [11.0, 12.0]])
    return (arr1, arr2, arr3)


@pytest.fixture
def coords_float_mismatched_shapes():
    """3-tuple of mismatched float arrays."""
    arr1 = np.array([1.0, 2.0, 3.0])
    arr2 = np.array([[4.0, 5.0, 6.0]])
    arr3 = np.array([7.0, 8.0, 9.0])
    return (arr1, arr2, arr3)


@pytest.fixture
def coords_float_mismatched_lengths():
    """3-tuple of 1D float arrays with different lengths."""
    arr1 = np.array([1.0, 2.0, 3.0])
    arr2 = np.array([4.0, 5.0])
    arr3 = np.array([7.0, 8.0, 9.0])
    return (arr1, arr2, arr3)


# ============================================================================
# Random State Objects
# ============================================================================

@pytest.fixture
def random_state_seed_42():
    """RandomState with fixed seed 42."""
    return RandomState(42)


@pytest.fixture
def random_state_seed_0():
    """RandomState with seed 0."""
    return RandomState(0)


@pytest.fixture
def random_state_seed_none():
    """RandomState with None seed (uses system time)."""
    return RandomState(None)


@pytest.fixture
def random_state_seed_array():
    """RandomState with array seed."""
    return RandomState(np.array([1, 2, 3, 4, 5]))


@pytest.fixture
def random_state_default():
    """Default RandomState."""
    return RandomState()


# ============================================================================
# Invalid/Edge Case Inputs
# ============================================================================

@pytest.fixture
def empty_float_array():
    """Empty float array."""
    return np.array([])


@pytest.fixture
def empty_int_array():
    """Empty integer array."""
    return np.array([], dtype=np.int32)


@pytest.fixture
def unsorted_float_1d():
    """Unsorted 1D float array."""
    return np.array([1.0, 3.0, 2.0, 4.0])


@pytest.fixture
def unsorted_int_1d():
    """Unsorted 1D integer array."""
    return np.array([1, 3, 2, 4], dtype=np.int32)


@pytest.fixture
def reverse_sorted_float_1d():
    """Reverse sorted 1D float array."""
    return np.array([5.0, 4.0, 3.0, 2.0, 1.0])


@pytest.fixture
def reverse_sorted_int_1d():
    """Reverse sorted 1D integer array."""
    return np.array([5, 4, 3, 2, 1], dtype=np.int32)


@pytest.fixture
def partially_sorted_float_1d():
    """Partially sorted 1D float array."""
    return np.array([1.0, 2.0, 3.0, 2.5, 4.0])


# ============================================================================
# Type Conversion Test Data
# ============================================================================

@pytest.fixture
def int_array_for_float_conversion():
    """Integer array that can be converted to float."""
    return np.array([1, 2, 3], dtype=np.int32)


@pytest.fixture
def float32_array():
    """Float32 array."""
    return np.array([1.0, 2.0, 3.0], dtype=np.float32)


@pytest.fixture
def float64_array():
    """Float64 array."""
    return np.array([1.0, 2.0, 3.0], dtype=np.float64)


@pytest.fixture
def bool_array_for_int_conversion():
    """Boolean array that can be converted to int."""
    return np.array([True, False, True])
