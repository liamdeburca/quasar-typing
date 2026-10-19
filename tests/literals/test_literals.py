import pytest
from pydantic import BaseModel, ValidationError, TypeAdapter

from quasar_typing.literals import (
    Method,
    FWHMStrategy,
    Scale,
    Variant,
    BootstrapType,
    FluxComponent,
    FluxContributions,
    Suffix,
    MCMCSamplingMethod,
)


class TestMethodLiteral:
    """Tests for Method type - validates 'bootstrap' with string normalization"""

    def test_method_accepts_lowercase(self):
        """Method accepts lowercase 'bootstrap'."""
        adapter = TypeAdapter(Method)
        result = adapter.validate_python("bootstrap")
        assert result == "bootstrap"

    def test_method_accepts_uppercase(self):
        """Method accepts uppercase 'BOOTSTRAP' and normalizes it."""
        adapter = TypeAdapter(Method)
        result = adapter.validate_python("BOOTSTRAP")
        assert result == "bootstrap"

    def test_method_accepts_mixed_case(self):
        """Method accepts mixed case 'BootStrap' and normalizes it."""
        adapter = TypeAdapter(Method)
        result = adapter.validate_python("BootStrap")
        assert result == "bootstrap"

    def test_method_strips_whitespace(self):
        """Method strips leading/trailing whitespace."""
        adapter = TypeAdapter(Method)
        result = adapter.validate_python("  bootstrap  ")
        assert result == "bootstrap"

    def test_method_strips_and_lowers(self):
        """Method both strips and lowers."""
        adapter = TypeAdapter(Method)
        result = adapter.validate_python("  BOOTSTRAP  ")
        assert result == "bootstrap"

    def test_method_rejects_invalid_value(self):
        """Method rejects values other than 'bootstrap'."""
        adapter = TypeAdapter(Method)
        with pytest.raises(ValidationError):
            adapter.validate_python("invalid")

    def test_method_rejects_wrong_case_not_stripped(self):
        """Method rejects unrelated values even after normalization."""
        adapter = TypeAdapter(Method)
        with pytest.raises(ValidationError):
            adapter.validate_python("something")

    def test_method_in_pydantic_model(self):
        """Method in Pydantic BaseModel."""
        class Config(BaseModel):
            method: Method

        config = Config(method="BOOTSTRAP")
        assert config.method == "bootstrap"

    def test_method_converts_int(self):
        """Method converts int to string and validates."""
        adapter = TypeAdapter(Method)
        # 123 as string is "123", which is not "bootstrap"
        with pytest.raises(ValidationError):
            adapter.validate_python(123)


class TestFWHMStrategy:
    """Tests for FWHMStrategy type - validates narrowest/average/widest with normalization"""

    def test_fwhm_strategy_accepts_narrowest_lowercase(self):
        """FWHMStrategy accepts lowercase 'narrowest'."""
        adapter = TypeAdapter(FWHMStrategy)
        result = adapter.validate_python("narrowest")
        assert result == "narrowest"

    def test_fwhm_strategy_accepts_narrowest_uppercase(self):
        """FWHMStrategy accepts uppercase 'NARROWEST' and normalizes."""
        adapter = TypeAdapter(FWHMStrategy)
        result = adapter.validate_python("NARROWEST")
        assert result == "narrowest"

    def test_fwhm_strategy_accepts_average_mixed_case(self):
        """FWHMStrategy accepts 'AveRage' and normalizes."""
        adapter = TypeAdapter(FWHMStrategy)
        result = adapter.validate_python("AveRage")
        assert result == "average"

    def test_fwhm_strategy_accepts_widest(self):
        """FWHMStrategy accepts 'widest'."""
        adapter = TypeAdapter(FWHMStrategy)
        result = adapter.validate_python("widest")
        assert result == "widest"

    def test_fwhm_strategy_strips_whitespace(self):
        """FWHMStrategy strips whitespace."""
        adapter = TypeAdapter(FWHMStrategy)
        result = adapter.validate_python("  average  ")
        assert result == "average"

    def test_fwhm_strategy_strips_and_lowers(self):
        """FWHMStrategy both strips and lowers."""
        adapter = TypeAdapter(FWHMStrategy)
        result = adapter.validate_python("  WIDEST  ")
        assert result == "widest"

    def test_fwhm_strategy_rejects_invalid(self):
        """FWHMStrategy rejects invalid values."""
        adapter = TypeAdapter(FWHMStrategy)
        with pytest.raises(ValidationError):
            adapter.validate_python("invalid")

    def test_fwhm_strategy_in_model(self):
        """FWHMStrategy in Pydantic model."""
        class Config(BaseModel):
            strategy: FWHMStrategy

        config = Config(strategy="  NARROWEST  ")
        assert config.strategy == "narrowest"


class TestScale:
    """Tests for Scale type - validates global/semilocal/local with normalization"""

    def test_scale_accepts_global(self):
        """Scale accepts 'global'."""
        adapter = TypeAdapter(Scale)
        result = adapter.validate_python("global")
        assert result == "global"

    def test_scale_accepts_semilocal_uppercase(self):
        """Scale accepts 'SEMILOCAL' and normalizes."""
        adapter = TypeAdapter(Scale)
        result = adapter.validate_python("SEMILOCAL")
        assert result == "semilocal"

    def test_scale_accepts_local_mixed_case(self):
        """Scale accepts 'LoCAL' and normalizes."""
        adapter = TypeAdapter(Scale)
        result = adapter.validate_python("LoCAL")
        assert result == "local"

    def test_scale_strips_whitespace(self):
        """Scale strips whitespace."""
        adapter = TypeAdapter(Scale)
        result = adapter.validate_python("  global  ")
        assert result == "global"

    def test_scale_rejects_invalid(self):
        """Scale rejects invalid values."""
        adapter = TypeAdapter(Scale)
        with pytest.raises(ValidationError):
            adapter.validate_python("globallocal")


class TestVariant:
    """Tests for Variant type - validates spectrum/standard/flexible/rigid"""

    def test_variant_accepts_spectrum(self):
        """Variant accepts 'spectrum'."""
        adapter = TypeAdapter(Variant)
        result = adapter.validate_python("spectrum")
        assert result == "spectrum"

    def test_variant_accepts_standard_uppercase(self):
        """Variant accepts 'STANDARD' and normalizes."""
        adapter = TypeAdapter(Variant)
        result = adapter.validate_python("STANDARD")
        assert result == "standard"

    def test_variant_accepts_flexible_mixed_case(self):
        """Variant accepts 'FlExiBLE' and normalizes."""
        adapter = TypeAdapter(Variant)
        result = adapter.validate_python("FlExiBLE")
        assert result == "flexible"

    def test_variant_accepts_rigid(self):
        """Variant accepts 'rigid'."""
        adapter = TypeAdapter(Variant)
        result = adapter.validate_python("rigid")
        assert result == "rigid"

    def test_variant_strips_whitespace(self):
        """Variant strips whitespace."""
        adapter = TypeAdapter(Variant)
        result = adapter.validate_python("  flexible  ")
        assert result == "flexible"

    def test_variant_rejects_invalid(self):
        """Variant rejects invalid values."""
        adapter = TypeAdapter(Variant)
        with pytest.raises(ValidationError):
            adapter.validate_python("unknown")


class TestBootstrapType:
    """Tests for BootstrapType type - validates spectrum/model/frequentist"""

    def test_bootstrap_type_accepts_spectrum(self):
        """BootstrapType accepts 'spectrum'."""
        adapter = TypeAdapter(BootstrapType)
        result = adapter.validate_python("spectrum")
        assert result == "spectrum"

    def test_bootstrap_type_accepts_model_uppercase(self):
        """BootstrapType accepts 'MODEL' and normalizes."""
        adapter = TypeAdapter(BootstrapType)
        result = adapter.validate_python("MODEL")
        assert result == "model"

    def test_bootstrap_type_accepts_frequentist_mixed_case(self):
        """BootstrapType accepts 'FREQUentist' and normalizes."""
        adapter = TypeAdapter(BootstrapType)
        result = adapter.validate_python("FREQUentist")
        assert result == "frequentist"

    def test_bootstrap_type_strips_whitespace(self):
        """BootstrapType strips whitespace."""
        adapter = TypeAdapter(BootstrapType)
        result = adapter.validate_python("  model  ")
        assert result == "model"


class TestFluxComponent:
    """Tests for FluxComponent type - validates pl/fe/ba/hg/em"""

    def test_flux_component_accepts_pl(self):
        """FluxComponent accepts 'pl'."""
        adapter = TypeAdapter(FluxComponent)
        result = adapter.validate_python("pl")
        assert result == "pl"

    def test_flux_component_accepts_fe_uppercase(self):
        """FluxComponent accepts 'FE' and normalizes."""
        adapter = TypeAdapter(FluxComponent)
        result = adapter.validate_python("FE")
        assert result == "fe"

    def test_flux_component_accepts_ba_mixed_case(self):
        """FluxComponent accepts 'Ba' and normalizes."""
        adapter = TypeAdapter(FluxComponent)
        result = adapter.validate_python("Ba")
        assert result == "ba"

    def test_flux_component_accepts_hg(self):
        """FluxComponent accepts 'hg'."""
        adapter = TypeAdapter(FluxComponent)
        result = adapter.validate_python("hg")
        assert result == "hg"

    def test_flux_component_accepts_em_uppercase(self):
        """FluxComponent accepts 'EM' and normalizes."""
        adapter = TypeAdapter(FluxComponent)
        result = adapter.validate_python("EM")
        assert result == "em"

    def test_flux_component_strips_whitespace(self):
        """FluxComponent strips whitespace."""
        adapter = TypeAdapter(FluxComponent)
        result = adapter.validate_python("  pl  ")
        assert result == "pl"

    def test_flux_component_rejects_invalid(self):
        """FluxComponent rejects invalid values."""
        adapter = TypeAdapter(FluxComponent)
        with pytest.raises(ValidationError):
            adapter.validate_python("invalid")


class TestFluxContributions:
    """Tests for FluxContributions type - frozenset of FluxComponent"""

    def test_flux_contributions_accepts_frozenset(self):
        """FluxContributions accepts frozenset of valid components."""
        adapter = TypeAdapter(FluxContributions)
        result = adapter.validate_python(frozenset(["pl", "fe", "ba"]))
        assert result == frozenset(["pl", "fe", "ba"])

    def test_flux_contributions_accepts_set(self):
        """FluxContributions accepts set and converts to frozenset."""
        adapter = TypeAdapter(FluxContributions)
        result = adapter.validate_python({"pl", "fe"})
        assert result == frozenset(["pl", "fe"])

    def test_flux_contributions_normalizes_case(self):
        """FluxContributions normalizes case."""
        adapter = TypeAdapter(FluxContributions)
        result = adapter.validate_python({"PL", "FE", "BA"})
        assert result == frozenset(["pl", "fe", "ba"])

    def test_flux_contributions_single_component(self):
        """FluxContributions with single component."""
        adapter = TypeAdapter(FluxContributions)
        result = adapter.validate_python({"em"})
        assert result == frozenset(["em"])

    def test_flux_contributions_all_components(self):
        """FluxContributions with all components."""
        adapter = TypeAdapter(FluxContributions)
        result = adapter.validate_python({"pl", "fe", "ba", "hg", "em"})
        assert result == frozenset(["pl", "fe", "ba", "hg", "em"])

    def test_flux_contributions_rejects_invalid(self):
        """FluxContributions rejects invalid component."""
        adapter = TypeAdapter(FluxContributions)
        with pytest.raises(ValidationError):
            adapter.validate_python({"pl", "invalid"})

    def test_flux_contributions_empty_set(self):
        """FluxContributions accepts empty frozenset."""
        adapter = TypeAdapter(FluxContributions)
        result = adapter.validate_python(frozenset())
        assert result == frozenset()


class TestSuffix:
    """Tests for Suffix type - validates raw/sc"""

    def test_suffix_accepts_raw(self):
        """Suffix accepts 'raw'."""
        adapter = TypeAdapter(Suffix)
        result = adapter.validate_python("raw")
        assert result == "raw"

    def test_suffix_accepts_sc_uppercase(self):
        """Suffix accepts 'SC' and normalizes."""
        adapter = TypeAdapter(Suffix)
        result = adapter.validate_python("SC")
        assert result == "sc"

    def test_suffix_accepts_raw_mixed_case(self):
        """Suffix accepts 'RaW' and normalizes."""
        adapter = TypeAdapter(Suffix)
        result = adapter.validate_python("RaW")
        assert result == "raw"

    def test_suffix_strips_whitespace(self):
        """Suffix strips whitespace."""
        adapter = TypeAdapter(Suffix)
        result = adapter.validate_python("  raw  ")
        assert result == "raw"

    def test_suffix_rejects_invalid(self):
        """Suffix rejects invalid values."""
        adapter = TypeAdapter(Suffix)
        with pytest.raises(ValidationError):
            adapter.validate_python("invalid")


class TestMCMCSamplingMethod:
    """Tests for MCMCSamplingMethod type - validates fisher/uniform"""

    def test_mcmc_accepts_fisher(self):
        """MCMCSamplingMethod accepts 'fisher'."""
        adapter = TypeAdapter(MCMCSamplingMethod)
        result = adapter.validate_python("fisher")
        assert result == "fisher"

    def test_mcmc_accepts_uniform_uppercase(self):
        """MCMCSamplingMethod accepts 'UNIFORM' and normalizes."""
        adapter = TypeAdapter(MCMCSamplingMethod)
        result = adapter.validate_python("UNIFORM")
        assert result == "uniform"

    def test_mcmc_accepts_fisher_mixed_case(self):
        """MCMCSamplingMethod accepts 'FisHer' and normalizes."""
        adapter = TypeAdapter(MCMCSamplingMethod)
        result = adapter.validate_python("FisHer")
        assert result == "fisher"

    def test_mcmc_strips_whitespace(self):
        """MCMCSamplingMethod strips whitespace."""
        adapter = TypeAdapter(MCMCSamplingMethod)
        result = adapter.validate_python("  uniform  ")
        assert result == "uniform"

    def test_mcmc_rejects_invalid(self):
        """MCMCSamplingMethod rejects invalid values."""
        adapter = TypeAdapter(MCMCSamplingMethod)
        with pytest.raises(ValidationError):
            adapter.validate_python("invalid")


class TestLiteralsInModels:
    """Tests for using multiple literal types in Pydantic models"""

    def test_multiple_literals_in_model(self):
        """Multiple literal types in single model."""
        class Config(BaseModel):
            method: Method
            strategy: FWHMStrategy
            scale: Scale
            variant: Variant
            bootstrap: BootstrapType

        config = Config(
            method="  BOOTSTRAP  ",
            strategy="NARROWEST",
            scale="semilocal",
            variant="  STANDARD  ",
            bootstrap="MODEL"
        )
        
        assert config.method == "bootstrap"
        assert config.strategy == "narrowest"
        assert config.scale == "semilocal"
        assert config.variant == "standard"
        assert config.bootstrap == "model"

    def test_literals_with_flux_in_model(self):
        """Literal types with flux-related types in model (excluding FluxContributions)."""
        class Config(BaseModel):
            component: FluxComponent
            suffix: Suffix

        config = Config(
            component="  PL  ",
            suffix="RAW"
        )
        
        assert config.component == "pl"
        assert config.suffix == "raw"

    def test_nested_model_with_literals(self):
        """Nested model with literal types."""
        class Inner(BaseModel):
            method: Method
            strategy: FWHMStrategy

        class Outer(BaseModel):
            inner: Inner
            variant: Variant

        outer = Outer(
            inner={"method": "BOOTSTRAP", "strategy": "AVERAGE"},
            variant="FLEXIBLE"
        )
        
        assert outer.inner.method == "bootstrap"
        assert outer.inner.strategy == "average"
        assert outer.variant == "flexible"

    def test_optional_literal(self):
        """Optional literal field in model."""
        from typing import Optional
        
        class Config(BaseModel):
            method: Optional[Method] = None

        config1 = Config()
        assert config1.method is None

        config2 = Config(method="BOOTSTRAP")
        assert config2.method == "bootstrap"

    def test_literal_with_default(self):
        """Literal field with default value."""
        class Config(BaseModel):
            scale: Scale = "global"

        config1 = Config()
        assert config1.scale == "global"

        config2 = Config(scale="SEMILOCAL")
        assert config2.scale == "semilocal"
