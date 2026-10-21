"""Tests for CosmologyType validator and integration scenarios."""

from typing import Optional

import pytest
from astropy.cosmology import WMAP1, WMAP9, Planck13, Planck15, Planck18
from pydantic import BaseModel, ConfigDict, ValidationError

from quasar_typing.astropy import (
    CosmologyName,
    CosmologyType,
    StrictCosmologyName,
)


class TestCosmologyType:
    """Tests for Cosmology instance type validation."""

    def test_accepts_wmap9_instance(self):
        """Validate that a WMAP9 Cosmology instance is accepted."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            cosmology: CosmologyType

        config = Config(cosmology=WMAP9)
        assert config.cosmology is WMAP9

    def test_accepts_wmap1_instance(self):
        """Validate that a WMAP1 Cosmology instance is accepted."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            cosmology: CosmologyType

        config = Config(cosmology=WMAP1)
        assert config.cosmology is WMAP1

    def test_accepts_planck13_instance(self):
        """Validate that a Planck13 Cosmology instance is accepted."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            cosmology: CosmologyType

        config = Config(cosmology=Planck13)
        assert config.cosmology is Planck13

    def test_accepts_planck15_instance(self):
        """Validate that a Planck15 Cosmology instance is accepted."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            cosmology: CosmologyType

        config = Config(cosmology=Planck15)
        assert config.cosmology is Planck15

    def test_accepts_planck18_instance(self):
        """Validate that a Planck18 Cosmology instance is accepted."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            cosmology: CosmologyType

        config = Config(cosmology=Planck18)
        assert config.cosmology is Planck18

    def test_accepts_multiple_different_instances(self):
        """Validate that different Cosmology instances are accepted."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            instances: list[CosmologyType]

        instances = [WMAP1, WMAP9, Planck13, Planck15, Planck18]
        config = Config(instances=instances)
        assert config.instances == instances

    def test_rejects_none(self):
        """Validate that None is rejected."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            cosmology: CosmologyType

        with pytest.raises(ValidationError):
            Config(cosmology=None)

    def test_rejects_string(self):
        """Validate that string (even valid cosmology name) is rejected."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            cosmology: CosmologyType

        invalid_strings = ["WMAP9", "wmap9", "Planck15", "planck15"]
        for string_value in invalid_strings:
            with pytest.raises(ValidationError):
                Config(cosmology=string_value)

    def test_rejects_integer(self):
        """Validate that integer is rejected."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            cosmology: CosmologyType

        with pytest.raises(ValidationError):
            Config(cosmology=123)

    def test_rejects_float(self):
        """Validate that float is rejected."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            cosmology: CosmologyType

        with pytest.raises(ValidationError):
            Config(cosmology=1.23)

    def test_rejects_dict(self):
        """Validate that dict is rejected."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            cosmology: CosmologyType

        test_dicts = [
            {},
            {"name": "WMAP9"},
            {"type": "Cosmology"},
        ]
        for dict_value in test_dicts:
            with pytest.raises(ValidationError):
                Config(cosmology=dict_value)

    def test_rejects_list(self):
        """Validate that list is rejected."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            cosmology: CosmologyType

        with pytest.raises(ValidationError):
            Config(cosmology=[WMAP9])

    def test_rejects_custom_object(self):
        """Validate that random custom object is rejected."""
        class CustomObject:
            pass

        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            cosmology: CosmologyType

        with pytest.raises(ValidationError):
            Config(cosmology=CustomObject())

    def test_passthrough_verification_wmap9(self):
        """Validate that WMAP9 instance is passed through unchanged."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            cosmology: CosmologyType

        config = Config(cosmology=WMAP9)
        # Should be the exact same object (passthrough, not copy)
        assert config.cosmology is WMAP9
        assert id(config.cosmology) == id(WMAP9)

    def test_passthrough_verification_planck15(self):
        """Validate that Planck15 instance is passed through unchanged."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            cosmology: CosmologyType

        config = Config(cosmology=Planck15)
        # Should be the exact same object (passthrough, not copy)
        assert config.cosmology is Planck15
        assert id(config.cosmology) == id(Planck15)

    def test_in_model_with_cosmology_instance(self):
        """Validate CosmologyType field in a BaseModel."""
        class CosmologyConfig(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            cosmology: CosmologyType

        config = CosmologyConfig(cosmology=WMAP9)
        assert config.cosmology is WMAP9

    def test_in_model_multiple_cosmology_fields(self):
        """Validate multiple CosmologyType fields in a BaseModel."""
        class MultiCosmologyConfig(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            primary: CosmologyType
            secondary: CosmologyType

        config = MultiCosmologyConfig(primary=WMAP9, secondary=Planck15)
        assert config.primary is WMAP9
        assert config.secondary is Planck15

    def test_optional_cosmology_type_with_value(self):
        """Validate Optional[CosmologyType] with a value."""
        class ConfigWithOptional(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            cosmology: Optional[CosmologyType] = None

        config = ConfigWithOptional(cosmology=WMAP9)
        assert config.cosmology is WMAP9

    def test_optional_cosmology_type_without_value(self):
        """Validate Optional[CosmologyType] without a value (None)."""
        class ConfigWithOptional(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            cosmology: Optional[CosmologyType] = None

        config = ConfigWithOptional()
        assert config.cosmology is None

    def test_error_message_on_invalid_type(self):
        """Validate that error messages are informative for invalid types."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            cosmology: CosmologyType

        try:
            Config(cosmology="WMAP9")
            pytest.fail("Should have raised ValidationError")
        except ValidationError as e:
            error_str = str(e)
            # Should contain information about invalid input
            assert "WMAP9" in error_str or "validation" in error_str.lower() or "instance" in error_str.lower()


class TestCosmologyIntegration:
    """Integration tests combining multiple cosmology types."""

    def test_model_with_name_and_instance(self):
        """Validate model with both cosmology name and instance fields."""
        class CosmologyConfig(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            name: CosmologyName
            instance: CosmologyType

        config = CosmologyConfig(name="wmap9", instance=WMAP9)
        assert config.name == "WMAP9"
        assert config.instance is WMAP9

    def test_model_with_strict_and_flexible_names(self):
        """Validate model with both strict and flexible name types."""
        class MixedNameConfig(BaseModel):
            strict_name: StrictCosmologyName
            flexible_name: CosmologyName

        # Strict requires exact case
        config = MixedNameConfig(strict_name="WMAP9", flexible_name="wmap9")
        assert config.strict_name == "WMAP9"
        assert config.flexible_name == "WMAP9"

        # Flexible accepts lowercase
        config = MixedNameConfig(strict_name="Planck15", flexible_name="planck15")
        assert config.strict_name == "Planck15"
        assert config.flexible_name == "Planck15"

        # Strict rejects lowercase
        with pytest.raises(ValidationError):
            MixedNameConfig(strict_name="wmap9", flexible_name="WMAP9")

    def test_real_world_scenario_cosmology_config(self):
        """Real-world scenario: configuration model with cosmology data."""
        class CosmologyDataConfig(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            name: CosmologyName
            instance: CosmologyType
            description: Optional[str] = None

        # Create config with mixed-case name
        config = CosmologyDataConfig(
            name="plAnCk15",
            instance=Planck15,
            description="Planck 2015 cosmology"
        )
        assert config.name == "Planck15"
        assert config.instance is Planck15
        assert config.description == "Planck 2015 cosmology"

    def test_multiple_cosmology_names_in_model(self):
        """Validate model with multiple cosmology name fields."""
        class MultiNameConfig(BaseModel):
            primary: CosmologyName
            secondary: CosmologyName
            tertiary: CosmologyName

        config = MultiNameConfig(
            primary="wmap1",
            secondary="PlAnCk13",
            tertiary="WMAP9"
        )
        assert config.primary == "WMAP1"
        assert config.secondary == "Planck13"
        assert config.tertiary == "WMAP9"

    def test_cosmology_in_nested_model(self):
        """Validate cosmology types in nested model structures."""
        class InnerCosmologyConfig(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            name: CosmologyName
            instance: CosmologyType

        class OuterConfig(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            cosmology_config: InnerCosmologyConfig

        outer = OuterConfig(
            cosmology_config={
                "name": "wmap9",
                "instance": WMAP9
            }
        )
        assert outer.cosmology_config.name == "WMAP9"
        assert outer.cosmology_config.instance is WMAP9

    def test_list_of_cosmology_names(self):
        """Validate list of cosmology names in a model."""
        class MultiCosmologyListConfig(BaseModel):
            cosmologies: list[CosmologyName]

        config = MultiCosmologyListConfig(
            cosmologies=["wmap1", "PlAnCk13", "WMAP9", "planck18"]
        )
        assert config.cosmologies == ["WMAP1", "Planck13", "WMAP9", "Planck18"]

    def test_list_of_cosmology_instances(self):
        """Validate list of cosmology instances in a model."""
        class MultiCosmologyInstanceConfig(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            instances: list[CosmologyType]

        config = MultiCosmologyInstanceConfig(
            instances=[WMAP1, WMAP9, Planck13, Planck15, Planck18]
        )
        assert config.instances == [WMAP1, WMAP9, Planck13, Planck15, Planck18]

    def test_optional_fields_all_types(self):
        """Validate optional cosmology fields in a model."""
        class FullCosmologyConfig(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            strict_name: Optional[StrictCosmologyName] = None
            flexible_name: Optional[CosmologyName] = None
            instance: Optional[CosmologyType] = None

        # All None
        config = FullCosmologyConfig()
        assert config.strict_name is None
        assert config.flexible_name is None
        assert config.instance is None

        # All with values
        config = FullCosmologyConfig(
            strict_name="WMAP9",
            flexible_name="planck15",
            instance=WMAP9
        )
        assert config.strict_name == "WMAP9"
        assert config.flexible_name == "Planck15"
        assert config.instance is WMAP9

        # Mixed (some None, some with values)
        config = FullCosmologyConfig(
            strict_name="Planck13",
            flexible_name=None,
            instance=Planck13
        )
        assert config.strict_name == "Planck13"
        assert config.flexible_name is None
        assert config.instance is Planck13

    def test_validation_error_propagates_in_nested_model(self):
        """Validate that validation errors propagate correctly in nested structures."""
        class InnerConfig(BaseModel):
            name: CosmologyName

        class OuterConfig(BaseModel):
            inner: InnerConfig

        # Invalid cosmology name should raise at outer level
        with pytest.raises(ValidationError):
            OuterConfig(inner={"name": "invalid_cosmology"})

    def test_model_serialization_with_cosmology_types(self):
        """Validate model serialization with cosmology fields."""
        class CosmologyConfig(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            name: CosmologyName
            instance: CosmologyType

        config = CosmologyConfig(name="wmap9", instance=WMAP9)
        
        # Model can be dumped to dict
        data = config.model_dump()
        assert data["name"] == "WMAP9"
        # Instance is serialized - with arbitrary_types_allowed, astropy Cosmology 
        # instances get serialized to dicts, so we check the name field in the serialized data
        assert "WMAP9" in str(data["instance"])

    def test_model_json_serialization_name_only(self):
        """Validate JSON serialization of cosmology names."""
        class CosmologyNameConfig(BaseModel):
            name: CosmologyName

        config = CosmologyNameConfig(name="wmap9")
        json_str = config.model_dump_json()
        assert "WMAP9" in json_str

    def test_all_available_cosmologies_in_list(self):
        """Validate all 8 available cosmologies work in various contexts."""
        cosmology_names = ["WMAP1", "WMAP3", "WMAP5", "WMAP7", "WMAP9", "Planck13", "Planck15", "Planck18"]
        
        class CosmologyListConfig(BaseModel):
            names: list[CosmologyName]

        config = CosmologyListConfig(names=[c.lower() for c in cosmology_names])
        assert config.names == cosmology_names

    def test_cosmology_instances_with_all_variants(self):
        """Validate different cosmology instances work together."""
        instances = [WMAP1, WMAP9, Planck13, Planck15, Planck18]
        
        class CosmologyInstancesConfig(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            instances: list[CosmologyType]

        config = CosmologyInstancesConfig(instances=instances)
        assert config.instances == instances

    def test_mixed_case_with_instances_comprehensive(self):
        """Comprehensive test with mixed cases and instances."""
        class ComprehensiveConfig(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            names: list[CosmologyName]
            strict_name: StrictCosmologyName
            instance: CosmologyType

        config = ComprehensiveConfig(
            names=["wmap1", "PlAnCk15", "WMAP9"],
            strict_name="Planck13",
            instance=WMAP9
        )
        assert config.names == ["WMAP1", "Planck15", "WMAP9"]
        assert config.strict_name == "Planck13"
        assert config.instance is WMAP9
