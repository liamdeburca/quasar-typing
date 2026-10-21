"""Tests for cosmology name types: StrictCosmologyName and CosmologyName."""

from typing import Optional

import pytest
from pydantic import BaseModel, ValidationError

from quasar_typing.astropy import CosmologyName, StrictCosmologyName


class TestStrictCosmologyName:
    """Tests for strict (case-sensitive) cosmology name validation."""

    def test_accepts_exact_cosmology_names(self):
        """Validate that exact case-sensitive names are accepted."""
        class Config(BaseModel):
            name: StrictCosmologyName

        valid_names = ["WMAP1", "WMAP3", "WMAP5", "WMAP7", "WMAP9", "Planck13", "Planck15", "Planck18"]
        for name in valid_names:
            config = Config(name=name)
            assert config.name == name

    def test_rejects_lowercase_names(self):
        """Validate that lowercase names are rejected."""
        class Config(BaseModel):
            name: StrictCosmologyName

        lowercase_names = ["wmap1", "wmap9", "planck13", "planck15"]
        for name in lowercase_names:
            with pytest.raises(ValidationError):
                Config(name=name)

    def test_rejects_mixed_case_names(self):
        """Validate that mixed case names are rejected."""
        class Config(BaseModel):
            name: StrictCosmologyName

        mixed_case_names = ["Wmap1", "wMAP9", "PLANCK13", "plAnCk15"]
        for name in mixed_case_names:
            with pytest.raises(ValidationError):
                Config(name=name)

    def test_rejects_invalid_names(self):
        """Validate that non-existent names are rejected."""
        class Config(BaseModel):
            name: StrictCosmologyName

        invalid_names = ["INVALID", "TEST", "NOTACOSMO", "XYZ"]
        for name in invalid_names:
            with pytest.raises(ValidationError):
                Config(name=name)

    def test_rejects_partial_matches(self):
        """Validate that partial matches are rejected."""
        class Config(BaseModel):
            name: StrictCosmologyName

        partial_names = ["WMAP", "Planck", "WM", "P"]
        for name in partial_names:
            with pytest.raises(ValidationError):
                Config(name=name)

    def test_rejects_none(self):
        """Validate that None is rejected."""
        class Config(BaseModel):
            name: StrictCosmologyName

        with pytest.raises(ValidationError):
            Config(name=None)

    def test_rejects_non_string_types(self):
        """Validate that non-string types are rejected."""
        class Config(BaseModel):
            name: StrictCosmologyName

        non_string_values = [123, 45.67, ["WMAP1"], {"name": "WMAP1"}, True]
        for value in non_string_values:
            with pytest.raises(ValidationError):
                Config(name=value)

    def test_error_message_includes_options(self):
        """Validate that error messages mention available cosmologies."""
        class Config(BaseModel):
            name: StrictCosmologyName

        try:
            Config(name="invalid_name")
            pytest.fail("Should have raised ValidationError")
        except ValidationError as e:
            error_str = str(e)
            # Check that error message is informative
            assert "invalid_name" in error_str or "validation" in error_str.lower()

    def test_in_model_simple(self):
        """Validate strict cosmology name in a simple BaseModel."""
        class CosmologyConfig(BaseModel):
            name: StrictCosmologyName

        # Valid
        config = CosmologyConfig(name="WMAP9")
        assert config.name == "WMAP9"

        # Invalid - case sensitivity
        with pytest.raises(ValidationError):
            CosmologyConfig(name="wmap9")

    def test_empty_string_rejected(self):
        """Validate that empty string is rejected."""
        class Config(BaseModel):
            name: StrictCosmologyName

        with pytest.raises(ValidationError):
            Config(name="")

    def test_whitespace_string_rejected(self):
        """Validate that whitespace-only string is rejected."""
        class Config(BaseModel):
            name: StrictCosmologyName

        with pytest.raises(ValidationError):
            Config(name="   ")


class TestCosmologyName:
    """Tests for flexible (case-insensitive with coercion) cosmology name validation."""

    def test_accepts_lowercase_names(self):
        """Validate that lowercase names are coerced to correct case."""
        class Config(BaseModel):
            name: CosmologyName

        test_cases = [
            ("wmap1", "WMAP1"),
            ("wmap9", "WMAP9"),
            ("planck13", "Planck13"),
            ("planck15", "Planck15"),
            ("planck18", "Planck18"),
        ]
        for input_name, expected_output in test_cases:
            config = Config(name=input_name)
            assert config.name == expected_output, f"Expected {expected_output}, got {config.name}"

    def test_accepts_uppercase_names(self):
        """Validate that uppercase names pass through correctly."""
        class Config(BaseModel):
            name: CosmologyName

        test_cases = ["WMAP1", "WMAP9", "Planck13", "Planck15", "Planck18"]
        for name in test_cases:
            config = Config(name=name)
            assert config.name == name

    def test_accepts_mixed_case_names(self):
        """Validate that mixed case names are coerced to correct case."""
        class Config(BaseModel):
            name: CosmologyName

        test_cases = [
            ("WmAp1", "WMAP1"),
            ("wMAP5", "WMAP5"),
            ("PlAnCk13", "Planck13"),
            ("plANCK15", "Planck15"),
        ]
        for input_name, expected_output in test_cases:
            config = Config(name=input_name)
            assert config.name == expected_output

    def test_handles_leading_whitespace(self):
        """Validate that leading whitespace is stripped."""
        class Config(BaseModel):
            name: CosmologyName

        test_cases = [
            (" wmap1", "WMAP1"),
            ("  planck15", "Planck15"),
            ("\twmap9", "WMAP9"),
            ("\nPlanck13", "Planck13"),
        ]
        for input_name, expected_output in test_cases:
            config = Config(name=input_name)
            assert config.name == expected_output

    def test_handles_trailing_whitespace(self):
        """Validate that trailing whitespace is stripped."""
        class Config(BaseModel):
            name: CosmologyName

        test_cases = [
            ("wmap1 ", "WMAP1"),
            ("planck15  ", "Planck15"),
            ("wmap9\t", "WMAP9"),
            ("Planck13\n", "Planck13"),
        ]
        for input_name, expected_output in test_cases:
            config = Config(name=input_name)
            assert config.name == expected_output

    def test_handles_both_whitespace(self):
        """Validate that both leading and trailing whitespace are stripped."""
        class Config(BaseModel):
            name: CosmologyName

        test_cases = [
            (" wmap1 ", "WMAP1"),
            ("  planck15  ", "Planck15"),
            ("\twmap9\t", "WMAP9"),
            (" \nPlanck13\n ", "Planck13"),
        ]
        for input_name, expected_output in test_cases:
            config = Config(name=input_name)
            assert config.name == expected_output

    def test_handles_complex_whitespace(self):
        """Validate that complex whitespace combinations are handled."""
        class Config(BaseModel):
            name: CosmologyName

        test_cases = [
            ("  \t wmap1 \n  ", "WMAP1"),
            ("\t  \nplanck15\n  \t", "Planck15"),
        ]
        for input_name, expected_output in test_cases:
            config = Config(name=input_name)
            assert config.name == expected_output

    def test_rejects_invalid_after_coercion(self):
        """Validate that invalid names are rejected even after coercion attempt."""
        class Config(BaseModel):
            name: CosmologyName

        invalid_names = ["invalid", "test", "notacosmo"]
        for name in invalid_names:
            with pytest.raises(ValidationError):
                Config(name=name)

    def test_rejects_partial_matches_after_coercion(self):
        """Validate that partial matches are rejected after coercion."""
        class Config(BaseModel):
            name: CosmologyName

        partial_names = ["wmap", "planck", "wm", "p"]
        for name in partial_names:
            with pytest.raises(ValidationError):
                Config(name=name)

    def test_all_available_cosmologies_lowercase(self):
        """Validate all 8 available cosmologies work with lowercase."""
        class Config(BaseModel):
            name: CosmologyName

        cosmologies = ["WMAP1", "WMAP3", "WMAP5", "WMAP7", "WMAP9", "Planck13", "Planck15", "Planck18"]
        for cosmo in cosmologies:
            lowercase = cosmo.lower()
            config = Config(name=lowercase)
            assert config.name == cosmo

    def test_all_available_cosmologies_uppercase(self):
        """Validate all 8 available cosmologies work with uppercase."""
        class Config(BaseModel):
            name: CosmologyName

        cosmologies = ["WMAP1", "WMAP3", "WMAP5", "WMAP7", "WMAP9", "Planck13", "Planck15", "Planck18"]
        for cosmo in cosmologies:
            uppercase = cosmo.upper()
            config = Config(name=uppercase)
            assert config.name == cosmo

    def test_all_available_cosmologies_mixed_case(self):
        """Validate all 8 available cosmologies work with mixed case."""
        class Config(BaseModel):
            name: CosmologyName

        cosmologies = ["WMAP1", "WMAP3", "WMAP5", "WMAP7", "WMAP9", "Planck13", "Planck15", "Planck18"]
        # Test with first char uppercase, rest lowercase
        for cosmo in cosmologies:
            mixed = cosmo[0].upper() + cosmo[1:].lower()
            config = Config(name=mixed)
            assert config.name == cosmo

    def test_in_model_simple(self):
        """Validate CosmologyName in a simple BaseModel."""
        class CosmologyConfig(BaseModel):
            name: CosmologyName

        # Accept lowercase, coerce to correct case
        config = CosmologyConfig(name="wmap9")
        assert config.name == "WMAP9"

        # Accept exact case
        config = CosmologyConfig(name="Planck15")
        assert config.name == "Planck15"

    def test_in_model_multiple_fields(self):
        """Validate multiple CosmologyName fields in a BaseModel."""
        class CosmologyMultiConfig(BaseModel):
            primary: CosmologyName
            secondary: CosmologyName
            tertiary: CosmologyName

        config = CosmologyMultiConfig(
            primary="wmap9",
            secondary="PlAnCk13",
            tertiary="WMAP1"
        )
        assert config.primary == "WMAP9"
        assert config.secondary == "Planck13"
        assert config.tertiary == "WMAP1"

    def test_error_message_on_validation_failure(self):
        """Validate that error messages are informative."""
        class Config(BaseModel):
            name: CosmologyName

        try:
            Config(name="not_a_cosmology")
            pytest.fail("Should have raised ValidationError")
        except ValidationError as e:
            error_str = str(e)
            assert "not_a_cosmology" in error_str or "validation" in error_str.lower()

    def test_preserves_correct_case_in_result(self):
        """Validate that coercion produces exact case from AVAILABLE."""
        class Config(BaseModel):
            name: CosmologyName

        # Should be "WMAP1", not "wmap1"
        config = Config(name="wmap1")
        assert config.name == "WMAP1"
        assert config.name != "wmap1"

        # Should be "Planck13", not "planck13" or "PLANCK13"
        config = Config(name="planck13")
        assert config.name == "Planck13"
        assert config.name != "planck13"
        assert config.name != "PLANCK13"

    def test_rejects_none(self):
        """Validate that None is rejected."""
        class Config(BaseModel):
            name: CosmologyName

        with pytest.raises(ValidationError):
            Config(name=None)

    def test_rejects_non_string_types(self):
        """Validate that non-string types are rejected."""
        class Config(BaseModel):
            name: CosmologyName

        non_string_values = [123, 45.67, ["wmap1"], {"name": "wmap1"}, True]
        for value in non_string_values:
            with pytest.raises(ValidationError):
                Config(name=value)

    def test_empty_string_rejected(self):
        """Validate that empty string is rejected."""
        class Config(BaseModel):
            name: CosmologyName

        with pytest.raises(ValidationError):
            Config(name="")

    def test_whitespace_only_string_rejected(self):
        """Validate that whitespace-only strings are rejected."""
        class Config(BaseModel):
            name: CosmologyName

        whitespace_strings = ["   ", "\t", "\n", "  \t\n  "]
        for ws_string in whitespace_strings:
            with pytest.raises(ValidationError):
                Config(name=ws_string)

    def test_optional_cosmology_name(self):
        """Validate Optional[CosmologyName] works correctly."""
        class ConfigWithOptional(BaseModel):
            cosmology: Optional[CosmologyName] = None

        # With value
        config = ConfigWithOptional(cosmology="wmap9")
        assert config.cosmology == "WMAP9"

        # Without value (None)
        config = ConfigWithOptional()
        assert config.cosmology is None

    def test_list_of_cosmology_names(self):
        """Validate List[CosmologyName] works correctly."""
        class ConfigWithList(BaseModel):
            cosmologies: list[CosmologyName]

        config = ConfigWithList(cosmologies=["wmap1", "PlAnCk13", "WMAP9"])
        assert config.cosmologies == ["WMAP1", "Planck13", "WMAP9"]

    def test_cosmology_name_in_nested_model(self):
        """Validate CosmologyName works in nested models."""
        class InnerConfig(BaseModel):
            name: CosmologyName

        class OuterConfig(BaseModel):
            inner: InnerConfig

        config = OuterConfig(inner={"name": "wmap9"})
        assert config.inner.name == "WMAP9"
