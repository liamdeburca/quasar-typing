import sys
from importlib import import_module
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter

import_module("astropy")

_import_structure: dict[str, list[str]] = {
    "cosmology_name": ["CosmologyName", "StrictCosmologyName"],
    "cosmology_type": ["CosmologyType"]
}

if TYPE_CHECKING:
    from .cosmology_name import (  # noqa: F401
        CosmologyName,
        StrictCosmologyName,
    )
    from .cosmology_type import CosmologyType  # noqa: F401
else:
    sys.modules[__name__] = LazyImporter(
        __name__,
        __file__,
        _import_structure,
    )