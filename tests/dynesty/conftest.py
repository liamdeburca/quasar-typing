"""Shared test fixtures for dynesty submodule tests."""

import numpy as np
import pytest

try:
    import dynesty
except ImportError:
    pytest.skip("dynesty not installed", allow_module_level=True)


@pytest.fixture
def loglikelihood_simple():
    """Simple likelihood function for testing."""
    def logl(x):
        # Simple Gaussian likelihood centered at origin
        return -0.5 * np.sum(x**2)
    return logl


@pytest.fixture
def prior_transform_uniform():
    """Uniform prior transform from unit cube to [-5, 5]."""
    def ptform(u):
        # Transform from [0, 1] to [-5, 5] for each dimension
        return 10 * u - 5
    return ptform


@pytest.fixture
def nested_sampler_basic(loglikelihood_simple, prior_transform_uniform):
    """Basic NestedSampler instance."""
    ndim = 3
    sampler = dynesty.NestedSampler(
        loglikelihood_simple,
        prior_transform_uniform,
        ndim=ndim
    )
    return sampler


@pytest.fixture
def nested_sampler_with_args(loglikelihood_simple, prior_transform_uniform):
    """NestedSampler with different configuration."""
    ndim = 2
    sampler = dynesty.NestedSampler(
        loglikelihood_simple,
        prior_transform_uniform,
        ndim=ndim,
        bound='multi'
    )
    return sampler


@pytest.fixture
def dynamic_nested_sampler_basic(loglikelihood_simple, prior_transform_uniform):
    """Basic DynamicNestedSampler instance."""
    ndim = 3
    sampler = dynesty.DynamicNestedSampler(
        loglikelihood_simple,
        prior_transform_uniform,
        ndim=ndim
    )
    return sampler


@pytest.fixture
def dynamic_nested_sampler_with_args(loglikelihood_simple, prior_transform_uniform):
    """DynamicNestedSampler with custom configuration."""
    ndim = 2
    sampler = dynesty.DynamicNestedSampler(
        loglikelihood_simple,
        prior_transform_uniform,
        ndim=ndim,
        nlive=300,
        bound='balls',
        sample='slice'
    )
    return sampler
