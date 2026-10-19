"""Test dynesty type validation using pydantic TypeAdapter."""

import pytest
from pydantic import TypeAdapter, ValidationError

try:
    import dynesty
except ImportError:
    pytest.skip("dynesty not installed", allow_module_level=True)

from quasar_typing.dynesty import (
    DynamicNestedSamplerType,
    SamplerType,
)


class TestSamplerTypeValid:
    """Tests for valid Sampler inputs (from NestedSampler factory)."""

    def test_sampler_from_nested_sampler_valid(self, nested_sampler_basic):
        """Sampler instance from NestedSampler factory should pass validation."""
        adapter = TypeAdapter(SamplerType)
        result = adapter.validate_python(nested_sampler_basic)
        assert isinstance(result, dynesty.sampler.Sampler)

    def test_sampler_with_args_valid(self, nested_sampler_with_args):
        """Sampler with custom arguments should pass validation."""
        adapter = TypeAdapter(SamplerType)
        result = adapter.validate_python(nested_sampler_with_args)
        assert isinstance(result, dynesty.sampler.Sampler)

    def test_sampler_maintains_identity(self, nested_sampler_basic):
        """Validated Sampler should be the same object."""
        adapter = TypeAdapter(SamplerType)
        result = adapter.validate_python(nested_sampler_basic)
        assert result is nested_sampler_basic

    def test_sampler_has_attributes(self, nested_sampler_basic):
        """Validated Sampler should have expected attributes."""
        adapter = TypeAdapter(SamplerType)
        result = adapter.validate_python(nested_sampler_basic)
        assert hasattr(result, 'ndim')
        assert result.ndim == 3

    def test_sampler_different_ndim(self, nested_sampler_with_args):
        """Sampler with different ndim should pass validation."""
        adapter = TypeAdapter(SamplerType)
        result = adapter.validate_python(nested_sampler_with_args)
        assert result.ndim == 2


class TestSamplerTypeInvalid:
    """Tests for invalid Sampler inputs."""

    def test_sampler_rejects_none(self):
        """None should raise validation error."""
        adapter = TypeAdapter(SamplerType)
        with pytest.raises(ValidationError):
            adapter.validate_python(None)

    def test_sampler_rejects_dict(self):
        """Plain dict should raise validation error."""
        adapter = TypeAdapter(SamplerType)
        with pytest.raises(ValidationError):
            adapter.validate_python({"ndim": 3})

    def test_sampler_rejects_string(self):
        """String should raise validation error."""
        adapter = TypeAdapter(SamplerType)
        with pytest.raises(ValidationError):
            adapter.validate_python("not a sampler")

    def test_sampler_rejects_integer(self):
        """Integer should raise validation error."""
        adapter = TypeAdapter(SamplerType)
        with pytest.raises(ValidationError):
            adapter.validate_python(42)

    def test_sampler_rejects_dynamic_sampler(self, dynamic_nested_sampler_basic):
        """DynamicNestedSampler should raise validation error for SamplerType."""
        adapter = TypeAdapter(SamplerType)
        # DynamicNestedSampler is a different type, should fail
        with pytest.raises(ValidationError):
            adapter.validate_python(dynamic_nested_sampler_basic)



class TestDynamicNestedSamplerTypeValid:
    """Tests for valid DynamicNestedSampler inputs."""

    def test_dynamic_nested_sampler_basic_valid(self, dynamic_nested_sampler_basic):
        """Basic DynamicNestedSampler should pass validation."""
        adapter = TypeAdapter(DynamicNestedSamplerType)
        result = adapter.validate_python(dynamic_nested_sampler_basic)
        assert isinstance(result, dynesty.DynamicNestedSampler)

    def test_dynamic_nested_sampler_with_args_valid(self, dynamic_nested_sampler_with_args):
        """DynamicNestedSampler with custom arguments should pass validation."""
        adapter = TypeAdapter(DynamicNestedSamplerType)
        result = adapter.validate_python(dynamic_nested_sampler_with_args)
        assert isinstance(result, dynesty.DynamicNestedSampler)

    def test_dynamic_nested_sampler_maintains_identity(self, dynamic_nested_sampler_basic):
        """Validated DynamicNestedSampler should be the same object."""
        adapter = TypeAdapter(DynamicNestedSamplerType)
        result = adapter.validate_python(dynamic_nested_sampler_basic)
        assert result is dynamic_nested_sampler_basic

    def test_dynamic_nested_sampler_has_attributes(self, dynamic_nested_sampler_basic):
        """Validated DynamicNestedSampler should have expected attributes."""
        adapter = TypeAdapter(DynamicNestedSamplerType)
        result = adapter.validate_python(dynamic_nested_sampler_basic)
        assert hasattr(result, 'ndim')
        assert result.ndim == 3

    def test_dynamic_nested_sampler_different_config(self, dynamic_nested_sampler_with_args):
        """DynamicNestedSampler with different config should pass validation."""
        adapter = TypeAdapter(DynamicNestedSamplerType)
        result = adapter.validate_python(dynamic_nested_sampler_with_args)
        assert result.ndim == 2


class TestDynamicNestedSamplerTypeInvalid:
    """Tests for invalid DynamicNestedSampler inputs."""

    def test_dynamic_nested_sampler_rejects_none(self):
        """None should raise validation error."""
        adapter = TypeAdapter(DynamicNestedSamplerType)
        with pytest.raises(ValidationError):
            adapter.validate_python(None)

    def test_dynamic_nested_sampler_rejects_dict(self):
        """Plain dict should raise validation error."""
        adapter = TypeAdapter(DynamicNestedSamplerType)
        with pytest.raises(ValidationError):
            adapter.validate_python({"ndim": 3})

    def test_dynamic_nested_sampler_rejects_string(self):
        """String should raise validation error."""
        adapter = TypeAdapter(DynamicNestedSamplerType)
        with pytest.raises(ValidationError):
            adapter.validate_python("not a sampler")

    def test_dynamic_nested_sampler_rejects_integer(self):
        """Integer should raise validation error."""
        adapter = TypeAdapter(DynamicNestedSamplerType)
        with pytest.raises(ValidationError):
            adapter.validate_python(42)

    def test_dynamic_nested_sampler_rejects_nested_sampler(self, nested_sampler_basic):
        """NestedSampler should raise validation error for DynamicNestedSamplerType."""
        adapter = TypeAdapter(DynamicNestedSamplerType)
        with pytest.raises(ValidationError):
            adapter.validate_python(nested_sampler_basic)


class TestIntegration:
    """Integration tests for both sampler types."""

    def test_both_samplers_valid_separately(self, nested_sampler_basic, dynamic_nested_sampler_basic):
        """Both sampler types should validate correctly when tested separately."""
        adapter_sampler = TypeAdapter(SamplerType)
        adapter_dynamic = TypeAdapter(DynamicNestedSamplerType)
        
        sampler_result = adapter_sampler.validate_python(nested_sampler_basic)
        dynamic_result = adapter_dynamic.validate_python(dynamic_nested_sampler_basic)
        
        assert isinstance(sampler_result, dynesty.sampler.Sampler)
        assert isinstance(dynamic_result, dynesty.DynamicNestedSampler)

    def test_samplers_are_distinct_types(self, nested_sampler_basic, dynamic_nested_sampler_basic):
        """Sampler and DynamicNestedSampler should be distinct types."""
        adapter_sampler = TypeAdapter(SamplerType)
        adapter_dynamic = TypeAdapter(DynamicNestedSamplerType)
        
        # These should raise errors when used with the wrong type
        with pytest.raises(ValidationError):
            adapter_sampler.validate_python(dynamic_nested_sampler_basic)
        
        with pytest.raises(ValidationError):
            adapter_dynamic.validate_python(nested_sampler_basic)
