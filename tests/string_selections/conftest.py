import pytest
from typing import Literal

from quasar_typing.string_selections import (
    StringSelection,
    DataTypes,
    ModelTypes,
    BackgroundFlux,
    PowerLawModelParams,
    IronModelParams,
    BalmerModelParams,
    HostGalaxyModelParams,
    GaussianModelParams,
    VaryLines,
    OutLines,
    OutMeasures,
)


# ===== Fixtures for concrete StringSelection subclasses =====

@pytest.fixture
def data_types_all():
    """DataTypes with all options selected."""
    return DataTypes({"all"})


@pytest.fixture
def data_types_subset():
    """DataTypes with subset of options."""
    return DataTypes({"pl", "fe"})


@pytest.fixture
def data_types_exclude():
    """DataTypes with 'all' and exclusions."""
    return DataTypes({"all", "pl", "fe"})


@pytest.fixture
def model_types_single():
    """ModelTypes with single option."""
    return ModelTypes({"ba"})


@pytest.fixture
def background_flux_mixed():
    """BackgroundFlux with mixed options."""
    return BackgroundFlux({"hg", "em"})


@pytest.fixture
def power_law_params_both():
    """PowerLawModelParams with both options."""
    return PowerLawModelParams({"flux", "alpha"})


@pytest.fixture
def power_law_params_one():
    """PowerLawModelParams with one option."""
    return PowerLawModelParams({"flux"})


@pytest.fixture
def iron_params_full():
    """IronModelParams with all options."""
    return IronModelParams({"all"})


@pytest.fixture
def balmer_params_subset():
    """BalmerModelParams with subset."""
    return BalmerModelParams({"flux", "ratio"})


@pytest.fixture
def host_galaxy_params_all():
    """HostGalaxyModelParams with all."""
    return HostGalaxyModelParams({"all"})


@pytest.fixture
def gaussian_params_mixed():
    """GaussianModelParams with subset."""
    return GaussianModelParams({"strength", "fwhm_v"})


# ===== Fixtures for unbounded StringSelection =====

@pytest.fixture
def vary_lines_custom():
    """VaryLines with custom string values."""
    return VaryLines({"line1", "line2", "line3"})


@pytest.fixture
def vary_lines_with_all():
    """VaryLines with 'all' keyword."""
    return VaryLines({"all", "line1"})


@pytest.fixture
def out_lines_custom():
    """OutLines with custom values."""
    return OutLines({"emission", "absorption"})


@pytest.fixture
def out_measures_empty():
    """OutMeasures with 'all' (effectively all)."""
    return OutMeasures({"all"})


# ===== Fixtures for basic StringSelection =====

@pytest.fixture
def custom_string_selection_with_options():
    """Custom StringSelection subclass with fixed options."""
    class Colors(StringSelection[Literal["red", "green", "blue"]]):
        _string_options = ("red", "green", "blue")
    
    return Colors({"red", "green"})


@pytest.fixture
def custom_string_selection_all():
    """Custom StringSelection subclass with 'all'."""
    class Colors(StringSelection[Literal["red", "green", "blue"]]):
        _string_options = ("red", "green", "blue")
    
    return Colors({"all"})


@pytest.fixture
def custom_string_selection_exclude():
    """Custom StringSelection subclass with exclude logic."""
    class Colors(StringSelection[Literal["red", "green", "blue"]]):
        _string_options = ("red", "green", "blue")
    
    return Colors({"all", "red"})


@pytest.fixture
def unbounded_string_selection():
    """StringSelection without _string_options."""
    return StringSelection({"apple", "banana", "cherry"})
