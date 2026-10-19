"""Test sparse array type validation using pydantic TypeAdapter."""

import numpy as np
import pytest
from pydantic import TypeAdapter, ValidationError
from scipy import sparse

from quasar_typing.scipy import (
    BSRArray,
    COOArray,
    CSCArray,
    CSRArray,
    CSRMatrix,
    DIAArray,
    DOKArray,
    LILArray,
    SparseArray,
)


class TestCSRArrayValid:
    """Tests for valid CSR array inputs."""

    def test_csr_array_valid_basic(self, csr_array_basic):
        """Valid CSR array should pass validation."""
        adapter = TypeAdapter(CSRArray)
        result = adapter.validate_python(csr_array_basic)
        assert isinstance(result, sparse.csr_array)

    def test_csr_array_valid_identity(self):
        """Identity matrix as CSR array should pass."""
        arr = sparse.csr_array(np.eye(3))
        adapter = TypeAdapter(CSRArray)
        result = adapter.validate_python(arr)
        assert isinstance(result, sparse.csr_array)
        assert result.shape == (3, 3)

    def test_csr_array_maintains_shape(self, csr_array_basic):
        """CSR array should maintain shape after validation."""
        adapter = TypeAdapter(CSRArray)
        result = adapter.validate_python(csr_array_basic)
        assert result.shape == csr_array_basic.shape

    def test_csr_array_maintains_data(self, csr_array_basic):
        """CSR array should maintain data after validation."""
        adapter = TypeAdapter(CSRArray)
        result = adapter.validate_python(csr_array_basic)
        np.testing.assert_array_equal(result.data, csr_array_basic.data)


class TestCSRMatrixValid:
    """Tests for valid CSR matrix inputs."""

    def test_csr_matrix_valid_basic(self, csr_matrix_basic):
        """Valid CSR matrix should pass validation."""
        adapter = TypeAdapter(CSRMatrix)
        result = adapter.validate_python(csr_matrix_basic)
        assert isinstance(result, sparse.csr_matrix)

    def test_csr_matrix_valid_identity(self):
        """Identity matrix as CSR matrix should pass."""
        mat = sparse.csr_matrix(np.eye(3))
        adapter = TypeAdapter(CSRMatrix)
        result = adapter.validate_python(mat)
        assert isinstance(result, sparse.csr_matrix)

    def test_csr_matrix_maintains_shape(self, csr_matrix_basic):
        """CSR matrix should maintain shape after validation."""
        adapter = TypeAdapter(CSRMatrix)
        result = adapter.validate_python(csr_matrix_basic)
        assert result.shape == csr_matrix_basic.shape


class TestSparseArrayTypes:
    """Tests for other sparse array types."""

    def test_coo_array_valid(self, coo_array_basic):
        """Valid COO array should pass validation."""
        adapter = TypeAdapter(COOArray)
        result = adapter.validate_python(coo_array_basic)
        assert isinstance(result, sparse.coo_array)

    def test_csc_array_valid(self):
        """Valid CSC array should pass validation."""
        arr = sparse.csc_array(np.eye(3))
        adapter = TypeAdapter(CSCArray)
        result = adapter.validate_python(arr)
        assert isinstance(result, sparse.csc_array)

    def test_bsr_array_valid(self):
        """Valid BSR array should pass validation."""
        arr = sparse.bsr_array(np.eye(4))
        adapter = TypeAdapter(BSRArray)
        result = adapter.validate_python(arr)
        assert isinstance(result, sparse.bsr_array)

    def test_dia_array_valid(self):
        """Valid DIA array should pass validation."""
        arr = sparse.dia_array(np.eye(3))
        adapter = TypeAdapter(DIAArray)
        result = adapter.validate_python(arr)
        assert isinstance(result, sparse.dia_array)

    def test_dok_array_valid(self):
        """Valid DOK array should pass validation."""
        arr = sparse.dok_array(np.eye(3))
        adapter = TypeAdapter(DOKArray)
        result = adapter.validate_python(arr)
        assert isinstance(result, sparse.dok_array)

    def test_lil_array_valid(self):
        """Valid LIL array should pass validation."""
        arr = sparse.lil_array(np.eye(3))
        adapter = TypeAdapter(LILArray)
        result = adapter.validate_python(arr)
        assert isinstance(result, sparse.lil_array)


class TestSparseArrayInvalid:
    """Tests for invalid sparse array inputs."""

    def test_csr_array_rejects_dense_array(self):
        """Dense numpy array should raise validation error."""
        adapter = TypeAdapter(CSRArray)
        with pytest.raises(ValidationError):
            adapter.validate_python(np.eye(3))
    
    def test_csr_array_rejects_list(self):
        """List should raise validation error."""
        adapter = TypeAdapter(CSRArray)
        with pytest.raises(ValidationError):
            adapter.validate_python([[1, 0], [0, 1]])

    def test_csr_array_rejects_wrong_type(self):
        """COO array should fail CSR validation."""
        adapter = TypeAdapter(CSRArray)
        coo = sparse.coo_array(np.eye(3))
        with pytest.raises(ValidationError):
            adapter.validate_python(coo)

    def test_csr_matrix_rejects_csr_array(self):
        """CSR array should fail CSR matrix validation."""
        adapter = TypeAdapter(CSRMatrix)
        arr = sparse.csr_array(np.eye(3))
        with pytest.raises(ValidationError):
            adapter.validate_python(arr)

    def test_sparse_array_rejects_none(self):
        """None should raise validation error."""
        adapter = TypeAdapter(CSRArray)
        with pytest.raises(ValidationError):
            adapter.validate_python(None)


class TestSparseArrayConversion:
    """Tests for sparse array format conversions."""

    def test_csr_to_csc_conversion(self, csr_array_basic):
        """Can convert CSR array to CSC."""
        csc = csr_array_basic.tocsc()
        adapter = TypeAdapter(CSCArray)
        result = adapter.validate_python(csc)
        assert isinstance(result, sparse.csc_array)

    def test_csr_to_coo_conversion(self, csr_array_basic):
        """Can convert CSR array to COO."""
        coo = csr_array_basic.tocoo()
        adapter = TypeAdapter(COOArray)
        result = adapter.validate_python(coo)
        assert isinstance(result, sparse.coo_array)

    def test_sparse_array_type_accepts_all_formats(self, csr_array_basic):
        """SparseArray type should accept all sparse array formats."""
        adapter = TypeAdapter(SparseArray)
        
        # Test CSR
        result = adapter.validate_python(csr_array_basic)
        assert isinstance(result, sparse.sparray)
        
        # Test COO
        result = adapter.validate_python(csr_array_basic.tocoo())
        assert isinstance(result, sparse.sparray)
