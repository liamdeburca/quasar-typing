"""Unit tests for Array_ class and type aliases."""

import pytest
import numpy as np

from quasar_typing.numpy import (
    FloatArray, FloatVector, FloatMatrix, FloatCube,
    IntArray, IntVector, IntMatrix, IntCube,
    BoolArray, BoolVector, BoolMatrix, BoolCube,
)


class TestFloatArray:
    """Test Array_ validation for floating point arrays."""
    
    def test_valid_float_vector(self):
        """Valid 1D float array should pass validation."""
        arr = np.array([1.0, 2.0, 3.0])
        result = FloatArray._validate(arr)
        assert isinstance(result, np.ndarray)
        np.testing.assert_array_equal(result, arr)
    
    def test_valid_float_2d_array(self):
        """Valid 2D float array should pass validation."""
        arr = np.array([[1.0, 2.0], [3.0, 4.0]])
        result = FloatArray._validate(arr)
        assert result.ndim == 2
        assert result.shape == (2, 2)
    
    def test_valid_float_3d_array(self):
        """Valid 3D float array should pass validation."""
        arr = np.arange(24, dtype=float).reshape(2, 3, 4)
        result = FloatArray._validate(arr)
        assert result.ndim == 3
        assert result.shape == (2, 3, 4)
    
    def test_invalid_list_input(self):
        """Python list input should raise error."""
        with pytest.raises(Exception) as exc_info:
            FloatArray._validate([1.0, 2.0, 3.0])
        assert 'Expected numpy array' in str(exc_info.value)
    
    def test_invalid_tuple_input(self):
        """Tuple input should raise error."""
        with pytest.raises(Exception) as exc_info:
            FloatArray._validate((1.0, 2.0, 3.0))
        assert 'Expected numpy array' in str(exc_info.value)
    
    def test_invalid_string_input(self):
        """String input should raise error."""
        with pytest.raises(Exception) as exc_info:
            FloatArray._validate("not an array")
        assert 'Expected numpy array' in str(exc_info.value)
    
    def test_invalid_scalar_input(self):
        """Scalar input should raise error."""
        with pytest.raises(Exception) as exc_info:
            FloatArray._validate(42.0)
        assert 'Expected numpy array' in str(exc_info.value)
    
    def test_invalid_dict_input(self):
        """Dictionary input should raise error."""
        with pytest.raises(Exception) as exc_info:
            FloatArray._validate({"a": 1.0, "b": 2.0})
        assert 'Expected numpy array' in str(exc_info.value)
    
    def test_invalid_int_array(self):
        """Integer array should fail for FloatArray dtype check."""
        arr = np.array([1, 2, 3])
        with pytest.raises(Exception) as exc_info:
            FloatArray._validate(arr)
        assert 'Expected numpy array of dtype' in str(exc_info.value)
    
    def test_valid_float32_array(self):
        """Float32 array should pass (floating supertype)."""
        arr = np.array([1.0, 2.0, 3.0], dtype=np.float32)
        result = FloatArray._validate(arr)
        assert result.dtype == np.float32
    
    def test_valid_float64_array(self):
        """Float64 array should pass (floating supertype)."""
        arr = np.array([1.0, 2.0, 3.0], dtype=np.float64)
        result = FloatArray._validate(arr)
        assert result.dtype == np.float64


class TestFloatVector:
    """Test Array_ validation for 1D float arrays."""
    
    def test_valid_1d_float_array(self):
        """Valid 1D float array should pass."""
        arr = np.array([1.0, 2.0, 3.0])
        result = FloatVector._validate(arr)
        assert result.ndim == 1
        assert result.size == 3
    
    def test_valid_1d_single_element(self):
        """1D array with single element should pass."""
        arr = np.array([42.0])
        result = FloatVector._validate(arr)
        assert result.ndim == 1
        assert result.size == 1
    
    def test_valid_1d_large_array(self):
        """Large 1D array should pass."""
        arr = np.arange(10000, dtype=float)
        result = FloatVector._validate(arr)
        assert result.ndim == 1
        assert result.size == 10000
    
    def test_invalid_0d_scalar_array(self):
        """0D scalar array should fail."""
        arr = np.array(42.0)
        with pytest.raises(Exception) as exc_info:
            FloatVector._validate(arr)
        assert 'Expected numpy array of ndim 1' in str(exc_info.value)
    
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
    
    def test_invalid_4d_array(self):
        """4D array should fail for FloatVector."""
        arr = np.zeros((2, 2, 2, 2), dtype=float)
        with pytest.raises(Exception) as exc_info:
            FloatVector._validate(arr)
        assert 'Expected numpy array of ndim 1' in str(exc_info.value)


class TestFloatMatrix:
    """Test Array_ validation for 2D float arrays."""
    
    def test_valid_2d_square_array(self):
        """Valid 2x2 float array should pass."""
        arr = np.array([[1.0, 2.0], [3.0, 4.0]])
        result = FloatMatrix._validate(arr)
        assert result.ndim == 2
        assert result.shape == (2, 2)
    
    def test_valid_2d_rectangular_array(self):
        """Valid non-square 2D array should pass."""
        arr = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        result = FloatMatrix._validate(arr)
        assert result.ndim == 2
        assert result.shape == (2, 3)
    
    def test_valid_2d_single_row(self):
        """2D array with single row should pass."""
        arr = np.array([[1.0, 2.0, 3.0]])
        result = FloatMatrix._validate(arr)
        assert result.ndim == 2
        assert result.shape == (1, 3)
    
    def test_valid_2d_single_column(self):
        """2D array with single column should pass."""
        arr = np.array([[1.0], [2.0], [3.0]])
        result = FloatMatrix._validate(arr)
        assert result.ndim == 2
        assert result.shape == (3, 1)
    
    def test_invalid_1d_array(self):
        """1D array should fail for FloatMatrix."""
        arr = np.array([1.0, 2.0, 3.0])
        with pytest.raises(Exception) as exc_info:
            FloatMatrix._validate(arr)
        assert 'Expected numpy array of ndim 2' in str(exc_info.value)
    
    def test_invalid_3d_array(self):
        """3D array should fail for FloatMatrix."""
        arr = np.array([[[1.0, 2.0]]])
        with pytest.raises(Exception) as exc_info:
            FloatMatrix._validate(arr)
        assert 'Expected numpy array of ndim 2' in str(exc_info.value)


class TestFloatCube:
    """Test Array_ validation for 3D float arrays."""
    
    def test_valid_3d_cube(self):
        """Valid 3D array should pass."""
        arr = np.array([[[1.0, 2.0], [3.0, 4.0]]])
        result = FloatCube._validate(arr)
        assert result.ndim == 3
    
    def test_valid_3d_array_various_shapes(self):
        """Various 3D arrays should pass."""
        for shape in [(1, 1, 1), (2, 3, 4), (5, 5, 5)]:
            arr = np.ones(shape, dtype=float)
            result = FloatCube._validate(arr)
            assert result.ndim == 3
            assert result.shape == shape
    
    def test_invalid_1d_array(self):
        """1D array should fail for FloatCube."""
        arr = np.array([1.0, 2.0, 3.0])
        with pytest.raises(Exception) as exc_info:
            FloatCube._validate(arr)
        assert 'Expected numpy array of ndim 3' in str(exc_info.value)
    
    def test_invalid_2d_array(self):
        """2D array should fail for FloatCube."""
        arr = np.array([[1.0, 2.0], [3.0, 4.0]])
        with pytest.raises(Exception) as exc_info:
            FloatCube._validate(arr)
        assert 'Expected numpy array of ndim 3' in str(exc_info.value)
    
    def test_invalid_4d_array(self):
        """4D array should fail for FloatCube."""
        arr = np.ones((2, 2, 2, 2), dtype=float)
        with pytest.raises(Exception) as exc_info:
            FloatCube._validate(arr)
        assert 'Expected numpy array of ndim 3' in str(exc_info.value)


class TestIntArray:
    """Test Array_ validation for integer arrays."""
    
    def test_valid_int_array(self):
        """Valid integer array should pass."""
        arr = np.array([1, 2, 3])
        result = IntArray._validate(arr)
        assert isinstance(result, np.ndarray)
        np.testing.assert_array_equal(result, arr)
    
    def test_valid_int32_array(self):
        """Int32 array should pass."""
        arr = np.array([1, 2, 3], dtype=np.int32)
        result = IntArray._validate(arr)
        assert result.dtype == np.int32
    
    def test_valid_int64_array(self):
        """Int64 array should pass."""
        arr = np.array([1, 2, 3], dtype=np.int64)
        result = IntArray._validate(arr)
        assert result.dtype == np.int64
    
    def test_valid_uint_array(self):
        """Unsigned int array should pass (integer supertype)."""
        arr = np.array([1, 2, 3], dtype=np.uint32)
        result = IntArray._validate(arr)
        assert result.dtype == np.uint32
    
    def test_invalid_float_array(self):
        """Float array should fail for IntArray."""
        arr = np.array([1.5, 2.5, 3.5])
        with pytest.raises(Exception) as exc_info:
            IntArray._validate(arr)
        assert 'Expected numpy array of dtype' in str(exc_info.value)
    
    def test_invalid_bool_array(self):
        """Bool array should fail for IntArray."""
        arr = np.array([True, False, True])
        with pytest.raises(Exception) as exc_info:
            IntArray._validate(arr)
        assert 'Expected numpy array of dtype' in str(exc_info.value)
    
    def test_invalid_complex_array(self):
        """Complex array should fail for IntArray."""
        arr = np.array([1+2j, 3+4j])
        with pytest.raises(Exception) as exc_info:
            IntArray._validate(arr)
        assert 'Expected numpy array of dtype' in str(exc_info.value)


class TestIntVector:
    """Test Array_ validation for 1D integer arrays."""
    
    def test_valid_1d_int_array(self):
        """Valid 1D integer array should pass."""
        arr = np.array([1, 2, 3])
        result = IntVector._validate(arr)
        assert result.ndim == 1
    
    def test_invalid_float_1d_array(self):
        """Float 1D array should fail for IntVector."""
        arr = np.array([1.0, 2.0, 3.0])
        with pytest.raises(Exception) as exc_info:
            IntVector._validate(arr)
        assert 'Expected numpy array of dtype' in str(exc_info.value)
    
    def test_invalid_2d_int_array(self):
        """2D integer array should fail for IntVector."""
        arr = np.array([[1, 2], [3, 4]])
        with pytest.raises(Exception) as exc_info:
            IntVector._validate(arr)
        assert 'Expected numpy array of ndim 1' in str(exc_info.value)


class TestIntMatrix:
    """Test Array_ validation for 2D integer arrays."""
    
    def test_valid_2d_int_array(self):
        """Valid 2D integer array should pass."""
        arr = np.array([[1, 2], [3, 4]])
        result = IntMatrix._validate(arr)
        assert result.ndim == 2
    
    def test_invalid_float_2d_array(self):
        """Float 2D array should fail for IntMatrix."""
        arr = np.array([[1.0, 2.0], [3.0, 4.0]])
        with pytest.raises(Exception) as exc_info:
            IntMatrix._validate(arr)
        assert 'Expected numpy array of dtype' in str(exc_info.value)


class TestIntCube:
    """Test Array_ validation for 3D integer arrays."""
    
    def test_valid_3d_int_array(self):
        """Valid 3D integer array should pass."""
        arr = np.array([[[1, 2], [3, 4]]])
        result = IntCube._validate(arr)
        assert result.ndim == 3


class TestBoolArray:
    """Test Array_ validation for boolean arrays."""
    
    def test_valid_bool_array(self):
        """Valid boolean array should pass."""
        arr = np.array([True, False, True])
        result = BoolArray._validate(arr)
        assert isinstance(result, np.ndarray)
    
    def test_valid_bool_array_2d(self):
        """Valid 2D boolean array should pass."""
        arr = np.array([[True, False], [False, True]])
        result = BoolArray._validate(arr)
        assert result.ndim == 2
    
    def test_invalid_int_array(self):
        """Integer array should fail for BoolArray."""
        arr = np.array([1, 0, 1])
        with pytest.raises(Exception) as exc_info:
            BoolArray._validate(arr)
        assert 'Expected numpy array of dtype' in str(exc_info.value)
    
    def test_invalid_float_array(self):
        """Float array should fail for BoolArray."""
        arr = np.array([1.0, 0.0, 1.0])
        with pytest.raises(Exception) as exc_info:
            BoolArray._validate(arr)
        assert 'Expected numpy array of dtype' in str(exc_info.value)
    
    def test_invalid_string_array(self):
        """String array should fail for BoolArray."""
        arr = np.array(['True', 'False'])
        with pytest.raises(Exception) as exc_info:
            BoolArray._validate(arr)
        assert 'Expected numpy array of dtype' in str(exc_info.value)


class TestBoolVector:
    """Test Array_ validation for 1D boolean arrays."""
    
    def test_valid_1d_bool_array(self):
        """Valid 1D boolean array should pass."""
        arr = np.array([True, False, True])
        result = BoolVector._validate(arr)
        assert result.ndim == 1
    
    def test_invalid_2d_bool_array(self):
        """2D boolean array should fail for BoolVector."""
        arr = np.array([[True, False], [False, True]])
        with pytest.raises(Exception) as exc_info:
            BoolVector._validate(arr)
        assert 'Expected numpy array of ndim 1' in str(exc_info.value)


class TestBoolMatrix:
    """Test Array_ validation for 2D boolean arrays."""
    
    def test_valid_2d_bool_array(self):
        """Valid 2D boolean array should pass."""
        arr = np.array([[True, False], [False, True]])
        result = BoolMatrix._validate(arr)
        assert result.ndim == 2
    
    def test_invalid_1d_bool_array(self):
        """1D boolean array should fail for BoolMatrix."""
        arr = np.array([True, False, True])
        with pytest.raises(Exception) as exc_info:
            BoolMatrix._validate(arr)
        assert 'Expected numpy array of ndim 2' in str(exc_info.value)


class TestBoolCube:
    """Test Array_ validation for 3D boolean arrays."""
    
    def test_valid_3d_bool_array(self):
        """Valid 3D boolean array should pass."""
        arr = np.array([[[True, False]]])
        result = BoolCube._validate(arr)
        assert result.ndim == 3
    
    def test_invalid_2d_bool_array(self):
        """2D boolean array should fail for BoolCube."""
        arr = np.array([[True, False], [False, True]])
        with pytest.raises(Exception) as exc_info:
            BoolCube._validate(arr)
        assert 'Expected numpy array of ndim 3' in str(exc_info.value)
