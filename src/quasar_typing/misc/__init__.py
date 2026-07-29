__all__ = [
    "BackgroundFlux",
    "BalmerModelParams",
    "BootstrapType",
    "DataTypes",
    "FWHMStrategy",
    "FluxComponent",
    "FluxContributions",
    "HostGalaxyModelParams",
    "IronModelParams",
    "Method",
    "ModelTypes",
    "OutLines",
    "OutMeasures",
    "Pool_",
    "PowerLawModelParams",
    "Scale",
    "StringSelection",
    "Suffix",
    "Variant",
    "VaryLines",
]
from typing import Literal

from .literals import (
    BootstrapType,
    FluxComponent,
    FluxContributions,
    FWHMStrategy,
    Method,
    Scale,
    Suffix,
    Variant,
)
from .pool import Pool_
from .string_selection import StringSelection


class BackgroundFlux(StringSelection[Literal["pl", "fe", "ba", "hg", "em"]]):
    """
    Lorem ipsum...
    """

    _string_options = ("pl", "fe", "ba", "hg", "em")


class ModelTypes(StringSelection[Literal["pl", "fe", "ba", "hg", "em"]]):
    """
    Lorem ipsum...
    """

    _string_options = ("pl", "fe", "ba", "hg", "em")


class DataTypes(StringSelection[Literal["pl", "fe", "ba", "hg", "em"]]):
    """
    Lorem ipsum...
    """

    _string_options = ("pl", "fe", "ba", "hg", "em")


class VaryLines(StringSelection[str]):
    """
    Lorem ipsum...
    """


class OutLines(StringSelection[str]):
    """
    Lorem ipsum...
    """

    _string_options = ("pl", "fe", "ba", "hg", "em")


class OutMeasures(StringSelection[str]):
    """
    Lorem ipsum...
    """


class PowerLawModelParams(StringSelection[Literal["flux", "alpha"]]):
    """
    Lorem ipsum...
    """

    _string_options = ("flux", "alpha")


class BalmerModelParams(StringSelection[Literal["flux", "fwhm", "ratio"]]):
    """
    Lorem ipsum...
    """

    _string_options = ("flux", "fwhm", "ratio")


class IronModelParams(
    StringSelection[Literal["flux", "fwhm", "split", "left", "right"]]
):
    """
    Lorem ipsum...
    """

    _string_options = ("flux", "fwhm", "split", "left", "right")


class HostGalaxyModelParams(StringSelection[Literal["flux", "fwhm"]]):
    """
    Lorem ipsum...
    """

    _string_options = ("flux", "fwhm")
