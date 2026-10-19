"""Shared test fixtures for scipy submodule tests."""

import numpy as np
import pytest
from scipy.optimize import least_squares, OptimizeResult
from scipy.sparse import csr_matrix, csr_array, coo_array
from scipy.stats import norm, rv_histogram


@pytest.fixture
def optimize_result_basic():
    """Basic OptimizeResult from scipy.optimize.least_squares."""
    def residuals(x):
        return np.array([(x[0] - 2)**2, (x[1] - 3)**2])
    
    x0 = np.array([1.0, 2.0])
    result = least_squares(residuals, x0)
    return result


@pytest.fixture
def optimize_result_with_constraints():
    """OptimizeResult from constrained least_squares."""
    def residuals(x):
        return np.array([(x[0] - 1)**2, (x[1] - 1)**2])
    
    x0 = np.array([0.5, 0.5])
    result = least_squares(
        residuals,
        x0,
        bounds=([0, 0], [1, 1])
    )
    return result


@pytest.fixture
def csr_matrix_basic():
    """Basic sparse CSR matrix."""
    data = np.array([1, 2, 3, 4, 5, 6])
    indices = np.array([0, 2, 2, 0, 1, 2])
    indptr = np.array([0, 2, 3, 6])
    return csr_matrix((data, indices, indptr), shape=(3, 3))


@pytest.fixture
def csr_matrix_identity():
    """Sparse CSR identity matrix."""
    return csr_matrix(np.eye(5))


@pytest.fixture
def csr_matrix_single_element():
    """CSR matrix with single non-zero element."""
    return csr_matrix(np.array([[0, 1, 0], [0, 0, 0], [0, 0, 0]]))


@pytest.fixture
def csr_array_basic():
    """Basic sparse CSR array (newer scipy format)."""
    data = np.array([1, 2, 3, 4, 5, 6])
    indices = np.array([0, 2, 2, 0, 1, 2])
    indptr = np.array([0, 2, 3, 6])
    return csr_array((data, indices, indptr), shape=(3, 3))


@pytest.fixture
def coo_array_basic():
    """Basic sparse COO array."""
    row = np.array([0, 1, 2, 2])
    col = np.array([0, 1, 1, 2])
    data = np.array([1, 2, 3, 4])
    return coo_array((data, (row, col)), shape=(3, 3))


@pytest.fixture
def rv_histogram_basic():
    """Basic histogram-based random variable."""
    # Create a simple histogram
    bin_edges = np.array([0, 1, 2, 3, 4, 5])
    bin_values = np.array([1, 2, 3, 2, 1])
    return rv_histogram((bin_values, bin_edges))


@pytest.fixture
def rv_continuous_frozen_basic():
    """Frozen continuous distribution (normal)."""
    return norm(loc=0, scale=1)


@pytest.fixture
def rv_continuous_frozen_shifted():
    """Frozen continuous distribution with different parameters."""
    return norm(loc=10, scale=2)
