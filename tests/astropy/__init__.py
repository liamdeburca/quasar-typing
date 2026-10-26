import importlib

import pytest

try:
    importlib.import_module("astropy")
except ImportError:
    pytest.skip("Astropy is not installed", allow_module_level=True)