"""Test CoordsTuple type validation using pydantic validate_call."""

import numpy as np
import pytest
from pydantic import TypeAdapter, validate_call
from pydantic_core import PydanticCustomError, ValidationError

from quasar_typing.numpy import (
    FittableCoordsTuple,
    SpectrumCoordsTuple,
)

# ============================================================================
# SpectrumCoordsTuple (CoordsTuple[FloatVector]) Tests
# ============================================================================

def test_spectrum_coords_valid_matching_1d(coords_float_matching_1d):
    """Valid 3-tuple of matching 1D arrays should pass."""
    adapter = TypeAdapter(SpectrumCoordsTuple)
    result = adapter.validate_python(coords_float_matching_1d)
    assert len(result) == 3
    assert result[0].shape == result[1].shape == result[2].shape


def test_spectrum_coords_valid_single_element_arrays():
    """3-tuple of single element arrays should pass."""
    adapter = TypeAdapter(SpectrumCoordsTuple)
    arr1 = np.array([1.0])
    arr2 = np.array([2.0])
    arr3 = np.array([3.0])
    result = adapter.validate_python((arr1, arr2, arr3))
    assert all(arr.size == 1 for arr in result)


def test_spectrum_coords_invalid_1d_vs_2d(coords_float_mismatched_shapes):
    """1D and 2D arrays should fail shape check."""
    adapter = TypeAdapter(SpectrumCoordsTuple)
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        adapter.validate_python(coords_float_mismatched_shapes)


def test_spectrum_coords_invalid_different_lengths(coords_float_mismatched_lengths):
    """1D arrays with different lengths should fail."""
    adapter = TypeAdapter(SpectrumCoordsTuple)
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        adapter.validate_python(coords_float_mismatched_lengths)


def test_spectrum_coords_invalid_2d_different_dimensions():
    """2D arrays with different dimensions should fail."""
    adapter = TypeAdapter(SpectrumCoordsTuple)
    arr1 = np.array([[1.0, 2.0], [3.0, 4.0]])
    arr2 = np.array([[5.0, 6.0, 7.0], [8.0, 9.0, 10.0]])
    arr3 = np.array([[11.0, 12.0], [13.0, 14.0]])
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        adapter.validate_python((arr1, arr2, arr3))


def test_spectrum_coords_invalid_3d_arrays_different_shapes():
    """3D arrays with different shapes should fail."""
    adapter = TypeAdapter(SpectrumCoordsTuple)
    arr1 = np.ones((2, 3, 4))
    arr2 = np.ones((2, 3, 5))
    arr3 = np.ones((2, 3, 4))
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        adapter.validate_python((arr1, arr2, arr3))


def test_spectrum_coords_invalid_first_differs():
    """First array differs in shape."""
    adapter = TypeAdapter(SpectrumCoordsTuple)
    arr1 = np.array([1.0, 2.0])  # Different length
    arr2 = np.array([4.0, 5.0, 6.0])
    arr3 = np.array([7.0, 8.0, 9.0])
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        adapter.validate_python((arr1, arr2, arr3))


def test_spectrum_coords_invalid_second_differs():
    """Second array differs in shape."""
    adapter = TypeAdapter(SpectrumCoordsTuple)
    arr1 = np.array([1.0, 2.0, 3.0])
    arr2 = np.array([4.0, 5.0])  # Different length
    arr3 = np.array([7.0, 8.0, 9.0])
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        adapter.validate_python((arr1, arr2, arr3))


def test_spectrum_coords_invalid_third_differs():
    """Third array differs in shape."""
    adapter = TypeAdapter(SpectrumCoordsTuple)
    arr1 = np.array([1.0, 2.0, 3.0])
    arr2 = np.array([4.0, 5.0, 6.0])
    arr3 = np.array([7.0, 8.0])  # Different length
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        adapter.validate_python((arr1, arr2, arr3))


# ============================================================================
# FittableCoordsTuple Tests
# ============================================================================

def test_fittable_coords_valid_matching_1d_finite():
    """Valid 3-tuple of matching 1D finite arrays should pass."""
    adapter = TypeAdapter(FittableCoordsTuple)
    arr1 = np.array([1.0, 2.0, 3.0])
    arr2 = np.array([4.0, 5.0, 6.0])
    arr3 = np.array([7.0, 8.0, 9.0])
    result = adapter.validate_python((arr1, arr2, arr3))
    assert len(result) == 3
    assert result[0].shape == result[1].shape == result[2].shape


def test_fittable_coords_valid_matching_2d_finite():
    """Valid 3-tuple of matching 2D finite arrays should pass."""
    adapter = TypeAdapter(FittableCoordsTuple)
    arr1 = np.array([[1.0, 2.0], [3.0, 4.0]])
    arr2 = np.array([[5.0, 6.0], [7.0, 8.0]])
    arr3 = np.array([[9.0, 10.0], [11.0, 12.0]])
    result = adapter.validate_python((arr1, arr2, arr3))
    assert result[0].shape == (2, 2)
    assert all(arr.shape == (2, 2) for arr in result)


def test_fittable_coords_invalid_mismatched_shapes():
    """Mismatched shapes should fail."""
    adapter = TypeAdapter(FittableCoordsTuple)
    arr1 = np.array([1.0, 2.0, 3.0])
    arr2 = np.array([[4.0, 5.0, 6.0]])
    arr3 = np.array([7.0, 8.0, 9.0])
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        adapter.validate_python((arr1, arr2, arr3))


def test_fittable_coords_invalid_with_nan():
    """Arrays with NaN should fail fittable validation."""
    adapter = TypeAdapter(FittableCoordsTuple)
    arr1 = np.array([1.0, np.nan, 3.0])
    arr2 = np.array([4.0, 5.0, 6.0])
    arr3 = np.array([7.0, 8.0, 9.0])
    # Note: Shape check happens first, so this passes shape validation
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        adapter.validate_python((arr1, arr2, arr3))


def test_fittable_coords_invalid_with_inf():
    """Arrays with Inf should fail fittable validation."""
    adapter = TypeAdapter(FittableCoordsTuple)
    arr1 = np.array([1.0, np.inf, 3.0])
    arr2 = np.array([4.0, 5.0, 6.0])
    arr3 = np.array([7.0, 8.0, 9.0])
    # Shape check passes first
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        adapter.validate_python((arr1, arr2, arr3)) 


def test_fittable_coords_invalid_empty_arrays():
    """Empty arrays should fail fittable validation."""
    adapter = TypeAdapter(FittableCoordsTuple)
    arr1 = np.array([])
    arr2 = np.array([])
    arr3 = np.array([])
    # Shape check passes (all same empty shape)
    with pytest.raises((ValidationError, PydanticCustomError)) as exc_info:
        adapter.validate_python((arr1, arr2, arr3))


# ============================================================================
# Pydantic validate_call Tests
# ============================================================================

def test_validate_call_with_spectrum_coords():
    """Test validate_call with SpectrumCoordsTuple."""
    @validate_call
    def process_coords(coords: SpectrumCoordsTuple) -> float:
        # coords is a 3-tuple of FloatVectors
        return float((coords[0] + coords[1] + coords[2]).sum())
    
    arr1 = np.array([1.0, 2.0, 3.0])
    arr2 = np.array([4.0, 5.0, 6.0])
    arr3 = np.array([7.0, 8.0, 9.0])
    
    result = process_coords((arr1, arr2, arr3))
    assert result == 45.0


def test_validate_call_rejects_mismatched_shapes():
    """validate_call should reject mismatched shapes."""
    @validate_call
    def process_coords(coords: SpectrumCoordsTuple) -> float:
        return float((coords[0] + coords[1] + coords[2]).sum())
    
    arr1 = np.array([1.0, 2.0, 3.0])
    arr2 = np.array([4.0, 5.0])  # Different length
    arr3 = np.array([7.0, 8.0, 9.0])
    
    with pytest.raises(ValidationError):
        process_coords((arr1, arr2, arr3))


def test_validate_call_with_fittable_coords():
    """Test validate_call with FittableCoordsTuple."""
    @validate_call
    def process_fittable_coords(coords: FittableCoordsTuple) -> float:
        return float((coords[0] + coords[1] + coords[2]).sum())
    
    arr1 = np.array([1.0, 2.0, 3.0])
    arr2 = np.array([4.0, 5.0, 6.0])
    arr3 = np.array([7.0, 8.0, 9.0])
    
    result = process_fittable_coords((arr1, arr2, arr3))
    assert result == 45.0


def test_validate_call_rejects_empty_arrays_fittable():
    """validate_call should reject empty arrays for FittableCoordsTuple."""
    @validate_call
    def process_fittable_coords(coords: FittableCoordsTuple) -> float:
        return float((coords[0] + coords[1] + coords[2]).sum())

    tup = (np.array([]), np.array([]), np.array([]))
    with pytest.raises((ValidationError, PydanticCustomError)):
        process_fittable_coords(tup)


def test_validate_call_rejects_nan_fittable_coords():
    """validate_call should reject NaN for FittableCoordsTuple."""
    @validate_call
    def process_fittable_coords(coords: FittableCoordsTuple) -> float:
        return float((coords[0] + coords[1] + coords[2]).sum())
    
    arr1 = np.array([1.0, 2.0, np.nan])
    arr2 = np.array([4.0, 5.0, 6.0])
    arr3 = np.array([7.0, 8.0, 9.0])

    with pytest.raises((ValidationError, PydanticCustomError)):
        process_fittable_coords((arr1, arr2, arr3))


def test_validate_call_multiple_coords_different_types():
    """validate_call should work with different coord tuple types."""
    @validate_call
    def process_spectrum(spec: SpectrumCoordsTuple) -> float:
        return float(spec[0][0])
    
    @validate_call
    def process_fittable(fit: FittableCoordsTuple) -> float:
        return float(fit[0][0])
    
    arr1 = np.array([1.0, 2.0, 3.0])
    arr2 = np.array([4.0, 5.0, 6.0])
    arr3 = np.array([7.0, 8.0, 9.0])
    
    result_spec = process_spectrum((arr1, arr2, arr3))
    result_fit = process_fittable((arr1, arr2, arr3))
    
    assert result_spec == 1.0
    assert result_fit == 1.0


# ============================================================================
# Shape Validation Edge Cases
# ============================================================================

def test_coords_single_element_arrays():
    """Single-element arrays should match shape."""
    adapter = TypeAdapter(SpectrumCoordsTuple)
    arr1 = np.array([1.0])
    arr2 = np.array([2.0])
    arr3 = np.array([3.0])
    result = adapter.validate_python((arr1, arr2, arr3))
    assert all(arr.size == 1 for arr in result)


def test_coords_large_matching_1d_arrays():
    """Large matching 1D arrays should pass."""
    adapter = TypeAdapter(SpectrumCoordsTuple)
    arr1 = np.arange(1000, dtype=float)
    arr2 = np.arange(1000, dtype=float) + 1000
    arr3 = np.arange(1000, dtype=float) + 2000
    result = adapter.validate_python((arr1, arr2, arr3))
    assert all(arr.size == 1000 for arr in result)


def test_coords_identity_arrays():
    """All identical arrays should definitely match."""
    adapter = TypeAdapter(SpectrumCoordsTuple)
    arr = np.array([1.0, 2.0, 3.0])
    result = adapter.validate_python((arr, arr, arr))
    assert all(result[i] is arr for i in range(3))


def test_coords_broadcast_incompatible():
    """Different shapes that can't broadcast should fail."""
    adapter = TypeAdapter(SpectrumCoordsTuple)
    arr1 = np.array([1.0, 2.0, 3.0, 4.0])
    arr2 = np.array([5.0, 6.0, 7.0])  # Different length
    arr3 = np.array([8.0, 9.0, 10.0, 11.0])
    
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python((arr1, arr2, arr3))
