"""Test OptimizeResultType validation using pydantic TypeAdapter."""

import numpy as np
import pytest
from pydantic import TypeAdapter, ValidationError

from quasar_typing.scipy.optimize import OptimizeResultType


class TestOptimizeResultTypeValid:
    """Tests for valid OptimizeResult inputs."""

    def test_optimize_result_valid_basic(self, optimize_result_basic):
        """Valid OptimizeResult should pass validation."""
        adapter = TypeAdapter(OptimizeResultType)
        result = adapter.validate_python(optimize_result_basic)
        assert isinstance(result, OptimizeResultType)
        assert hasattr(result, 'x')
        assert hasattr(result, 'fun')

    def test_optimize_result_valid_with_constraints(self, optimize_result_with_constraints):
        """OptimizeResult from constrained optimization should pass."""
        adapter = TypeAdapter(OptimizeResultType)
        result = adapter.validate_python(optimize_result_with_constraints)
        assert isinstance(result, OptimizeResultType)
        assert result.success is not None
        assert result.message is not None

    def test_optimize_result_maintains_attributes(self, optimize_result_basic):
        """Validated OptimizeResult should maintain all attributes."""
        adapter = TypeAdapter(OptimizeResultType)
        result = adapter.validate_python(optimize_result_basic)
        original = optimize_result_basic
        
        np.testing.assert_array_equal(result.x, original.x)
        assert result.success == original.success
        assert result.nfev == original.nfev

    def test_optimize_result_has_dof_property(self, optimize_result_basic):
        """Validated OptimizeResult should have dof property."""
        adapter = TypeAdapter(OptimizeResultType)
        result = adapter.validate_python(optimize_result_basic)
        dof = result.dof
        assert isinstance(dof, int)

    def test_optimize_result_has_chi2_property(self, optimize_result_basic):
        """Validated OptimizeResult should have chi2 property."""
        adapter = TypeAdapter(OptimizeResultType)
        result = adapter.validate_python(optimize_result_basic)
        chi2 = result.chi2
        assert isinstance(chi2, (int, float, np.number))
        assert chi2 >= 0

    def test_optimize_result_has_reduced_chi2_property(self, optimize_result_basic):
        """Validated OptimizeResult should have reduced_chi2 property."""
        adapter = TypeAdapter(OptimizeResultType)
        result = adapter.validate_python(optimize_result_basic)
        reduced_chi2 = result.reduced_chi2
        assert isinstance(reduced_chi2, (int, float, np.number))


class TestOptimizeResultTypeInvalid:
    """Tests for invalid OptimizeResult inputs."""

    def test_optimize_result_rejects_dict(self):
        """Plain dict should raise validation error."""
        adapter = TypeAdapter(OptimizeResultType)
        with pytest.raises(ValidationError):
            adapter.validate_python({'x': [1, 2], 'fun': [0.1]})

    def test_optimize_result_rejects_none(self):
        """None should raise validation error."""
        adapter = TypeAdapter(OptimizeResultType)
        with pytest.raises(ValidationError):
            adapter.validate_python(None)

    def test_optimize_result_rejects_array(self):
        """NumPy array should raise validation error."""
        adapter = TypeAdapter(OptimizeResultType)
        with pytest.raises(ValidationError):
            adapter.validate_python(np.array([1, 2, 3]))

    def test_optimize_result_rejects_string(self):
        """String should raise validation error."""
        adapter = TypeAdapter(OptimizeResultType)
        with pytest.raises(ValidationError):
            adapter.validate_python("not an optimize result")


class TestOptimizeResultTypeProperties:
    """Tests for OptimizeResultType computed properties."""

    def test_chi2_calculation(self, optimize_result_basic):
        """chi2 property should compute dot product of fun."""
        adapter = TypeAdapter(OptimizeResultType)
        result = adapter.validate_python(optimize_result_basic)
        expected_chi2 = np.dot(result.fun, result.fun)
        assert np.isclose(result.chi2, expected_chi2)

    def test_dof_calculation(self, optimize_result_basic):
        """dof (degrees of freedom) should be fun.size - x.size."""
        adapter = TypeAdapter(OptimizeResultType)
        result = adapter.validate_python(optimize_result_basic)
        expected_dof = result.fun.size - result.x.size
        assert result.dof == expected_dof

    def test_reduced_chi2_finite(self, optimize_result_basic):
        """reduced_chi2 should be finite when dof > 0."""
        adapter = TypeAdapter(OptimizeResultType)
        result = adapter.validate_python(optimize_result_basic)
        if result.dof > 0:
            assert np.isfinite(result.reduced_chi2)

    def test_active_mask_properties(self, optimize_result_with_constraints):
        """active_mask-related properties should work when mask exists."""
        adapter = TypeAdapter(OptimizeResultType)
        result = adapter.validate_python(optimize_result_with_constraints)
        # These properties should not raise even if active_mask is None
        n_lb = result.n_lb
        n_ub = result.n_ub
        assert isinstance(n_lb, int)
        assert isinstance(n_ub, int)
