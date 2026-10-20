"""Test scipy.stats type validation using pydantic TypeAdapter."""

import numpy as np
import pytest
from pydantic import TypeAdapter, ValidationError
from scipy.stats import norm, rv_histogram, uniform

from quasar_typing.scipy.stats import (
    RVContinuous,
    RVContinuousFrozen,
    RVHistogram,
)


class TestRVContinuousFrozenValid:
    """Tests for valid rv_continuous_frozen inputs."""

    def test_rv_continuous_frozen_normal(self, rv_continuous_frozen_basic):
        """Frozen normal distribution should pass validation."""
        adapter = TypeAdapter(RVContinuousFrozen)
        result = adapter.validate_python(rv_continuous_frozen_basic)
        assert result is not None
        # Check that it behaves like a frozen RV
        pdf_result = result.pdf(0)
        assert isinstance(pdf_result, (float, np.floating))

    def test_rv_continuous_frozen_shifted(self, rv_continuous_frozen_shifted):
        """Frozen distribution with different parameters should pass."""
        adapter = TypeAdapter(RVContinuousFrozen)
        result = adapter.validate_python(rv_continuous_frozen_shifted)
        assert result is not None

    def test_rv_continuous_frozen_uniform(self):
        """Frozen uniform distribution should pass."""
        rv = uniform(loc=0, scale=1)
        adapter = TypeAdapter(RVContinuousFrozen)
        result = adapter.validate_python(rv)
        assert result is not None
        assert result.ppf(0.5) == pytest.approx(0.5)

    def test_rv_continuous_frozen_maintains_params(self):
        """Frozen RV should maintain its parameters."""
        rv = norm(loc=5, scale=2)
        adapter = TypeAdapter(RVContinuousFrozen)
        result = adapter.validate_python(rv)
        # Check that the distribution has correct properties
        mean = result.ppf(0.5)  # median at quantile 0.5
        assert result.pdf(5) > 0  # PDF should be positive at mean


class TestRVContinuousValid:
    """Tests for valid rv_continuous inputs."""

    def test_rv_continuous_norm_distribution(self):
        """norm distribution should pass validation."""
        adapter = TypeAdapter(RVContinuous)
        result = adapter.validate_python(norm)
        assert result is not None

    def test_rv_continuous_uniform_distribution(self):
        """uniform distribution should pass validation."""
        adapter = TypeAdapter(RVContinuous)
        result = adapter.validate_python(uniform)
        assert result is not None

    def test_rv_continuous_is_instance(self):
        """RVContinuous should validate instances correctly."""
        adapter = TypeAdapter(RVContinuous)
        # norm is an instance of rv_continuous
        result = adapter.validate_python(norm)
        assert result is norm


class TestRVHistogramValid:
    """Tests for valid rv_histogram inputs."""

    def test_rv_histogram_valid_basic(self, rv_histogram_basic):
        """Valid rv_histogram should pass validation."""
        adapter = TypeAdapter(RVHistogram)
        result = adapter.validate_python(rv_histogram_basic)
        assert result is not None
        # Should be callable (can sample/evaluate)
        assert callable(result.pdf)

    def test_rv_histogram_can_sample(self, rv_histogram_basic):
        """RV histogram should be able to produce samples."""
        adapter = TypeAdapter(RVHistogram)
        result = adapter.validate_python(rv_histogram_basic)
        samples = result.rvs(size=10)
        assert len(samples) == 10

    def test_rv_histogram_can_evaluate_pdf(self, rv_histogram_basic):
        """RV histogram should be able to evaluate PDF."""
        adapter = TypeAdapter(RVHistogram)
        result = adapter.validate_python(rv_histogram_basic)
        x = np.array([1.0, 2.0, 3.0])
        pdf_values = result.pdf(x)
        assert len(pdf_values) == len(x)

    def test_rv_histogram_from_data(self):
        """RV histogram created from data should pass validation."""
        bin_edges = np.array([0, 1, 2, 3, 4])
        bin_values = np.array([1, 2, 3, 2])
        rv = rv_histogram((bin_values, bin_edges))
        adapter = TypeAdapter(RVHistogram)
        result = adapter.validate_python(rv)
        assert result is not None


class TestRVTypesInvalid:
    """Tests for invalid RV inputs."""

    def test_rv_continuous_frozen_rejects_frozen_normal(self):
        """Plain dict should fail validation."""
        adapter = TypeAdapter(RVContinuousFrozen)
        with pytest.raises(ValidationError):
            adapter.validate_python({})

    def test_rv_continuous_frozen_rejects_array(self):
        """Array should fail validation."""
        adapter = TypeAdapter(RVContinuousFrozen)
        with pytest.raises(ValidationError):
            adapter.validate_python(np.array([1, 2, 3]))

    def test_rv_continuous_rejects_dict(self):
        """Dict should fail RVContinuous validation."""
        adapter = TypeAdapter(RVContinuous)
        with pytest.raises(ValidationError):
            adapter.validate_python({})

    def test_rv_histogram_rejects_dict(self):
        """Dict should fail RVHistogram validation."""
        adapter = TypeAdapter(RVHistogram)
        with pytest.raises(ValidationError):
            adapter.validate_python({})

    def test_rv_histogram_rejects_none(self):
        """None should fail RVHistogram validation."""
        adapter = TypeAdapter(RVHistogram)
        with pytest.raises(ValidationError):
            adapter.validate_python(None)


class TestRVTypeCoercion:
    """Tests for type coercion and conversion."""

    def test_rv_continuous_frozen_creation_from_frozen(self):
        """Frozen RV created directly should pass."""
        rv = norm(loc=0, scale=1)
        adapter = TypeAdapter(RVContinuousFrozen)
        result = adapter.validate_python(rv)
        # Should remain the same
        assert result is rv

    def test_rv_histogram_samples_within_range(self, rv_histogram_basic):
        """Samples from RV histogram should be within histogram range."""
        adapter = TypeAdapter(RVHistogram)
        result = adapter.validate_python(rv_histogram_basic)
        samples = result.rvs(size=100)
        # Samples should be within [0, 5] range (from fixture)
        assert np.all(samples >= 0)
        assert np.all(samples <= 5)
