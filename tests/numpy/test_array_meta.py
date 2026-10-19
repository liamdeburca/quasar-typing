"""Test that Array type metadata is properly available during validation."""

from typing import get_args
import numpy as np
from pydantic import TypeAdapter
from quasar_typing.numpy import FloatArray, FloatVector, IntArray, BoolArray


def test_get_args_on_type_aliases():
    """Test what get_args returns for type aliases."""
    print(f"\nFloatArray: {FloatArray}")
    print(f"get_args(FloatArray): {get_args(FloatArray)}")
    print(f"FloatArray.__value__: {FloatArray.__value__}")
    print(f"get_args(FloatArray.__value__): {get_args(FloatArray.__value__)}")


def test_float_array_validation_with_int():
    """FloatArray should accept and coerce int32 to float64."""
    adapter = TypeAdapter(FloatArray)
    arr = np.array([1, 2, 3], dtype=np.int32)
    
    print(f"\nInput: dtype={arr.dtype}")
    result = adapter.validate_python(arr)
    print(f"Result: dtype={result.dtype}")
    
    assert result.dtype == np.float64


def test_float_vector_validation():
    """FloatVector should accept 1D float arrays."""
    adapter = TypeAdapter(FloatVector)
    arr = np.array([1.0, 2.0, 3.0], dtype=np.float32)
    
    print(f"\nInput: shape={arr.shape}, dtype={arr.dtype}")
    result = adapter.validate_python(arr)
    print(f"Result: shape={result.shape}, dtype={result.dtype}")
    
    # Should be float64 and 1D
    assert result.dtype == np.float64
    assert result.shape == (3,)


def test_int_array_validation():
    """IntArray should accept integer arrays."""
    adapter = TypeAdapter(IntArray)
    arr = np.array([1, 2, 3], dtype=np.int32)
    
    print(f"\nInput: dtype={arr.dtype}")
    result = adapter.validate_python(arr)
    print(f"Result: dtype={result.dtype}")
    
    # Should remain int64 (numpy's standard int)
    assert np.issubdtype(result.dtype, np.integer)


def test_bool_array_validation():
    """BoolArray should accept boolean arrays."""
    adapter = TypeAdapter(BoolArray)
    arr = np.array([True, False, True], dtype=np.bool_)
    
    print(f"\nInput: dtype={arr.dtype}")
    result = adapter.validate_python(arr)
    print(f"Result: dtype={result.dtype}")
    
    assert result.dtype == np.bool_
