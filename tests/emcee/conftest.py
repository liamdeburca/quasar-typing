"""Shared test fixtures for emcee submodule tests."""

import numpy as np
import pytest

try:
    import emcee
    from emcee import EnsembleSampler, backends, moves
except ImportError:
    pytest.skip("emcee not installed", allow_module_level=True)


@pytest.fixture
def simple_log_prob():
    """Simple log-probability function for testing."""
    def log_prob(x):
        # Simple quadratic: log_prob = -0.5 * sum(x^2)
        return -0.5 * np.sum(x**2)
    return log_prob


@pytest.fixture
def log_prob_with_args():
    """Log-probability function that accepts arguments."""
    def log_prob(x, mu, sigma):
        return -0.5 * np.sum(((x - mu) / sigma)**2)
    return log_prob


@pytest.fixture
def ensemble_sampler_basic(simple_log_prob):
    """Basic EnsembleSampler instance."""
    nwalkers = 32
    ndim = 3
    sampler = EnsembleSampler(nwalkers, ndim, simple_log_prob)
    return sampler


@pytest.fixture
def ensemble_sampler_with_backend(simple_log_prob):
    """EnsembleSampler with a memory backend."""
    nwalkers = 16
    ndim = 2
    backend = backends.Backend()
    sampler = EnsembleSampler(nwalkers, ndim, simple_log_prob, backend=backend)
    return sampler


@pytest.fixture
def ensemble_sampler_with_moves():
    """EnsembleSampler with custom moves."""
    def log_prob(x):
        return -0.5 * np.sum(x**2)
    
    nwalkers = 32
    ndim = 3
    # Create a list of moves
    move_list = [
        (moves.DEMove(), 0.8),
        (moves.DESnookerMove(), 0.2),
    ]
    sampler = EnsembleSampler(
        nwalkers, ndim, log_prob, moves=move_list
    )
    return sampler


@pytest.fixture
def move_de():
    """DE move instance."""
    return moves.DEMove()


@pytest.fixture
def move_de_snooker():
    """DE Snooker move instance."""
    return moves.DESnookerMove()


@pytest.fixture
def move_stretch():
    """Stretch move instance."""
    return moves.StretchMove()


@pytest.fixture
def backend_memory(simple_log_prob):
    """Memory backend instance."""
    ndim = 3
    nwalkers = 16
    backend = backends.Backend()
    # Initialize by creating a sampler with this backend
    EnsembleSampler(nwalkers, ndim, simple_log_prob, backend=backend)
    return backend


@pytest.fixture
def backend_hdf5(tmp_path):
    """HDF5 backend instance using temporary directory."""
    ndim = 2
    nwalkers = 8
    hdf_file = tmp_path / "test_backend.h5"
    try:
        return backends.HDFBackend(str(hdf_file), name="mcmc")
    except ImportError:
        pytest.skip("h5py not installed")
