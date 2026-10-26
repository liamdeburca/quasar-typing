import importlib

import pytest

try:
    importlib.import_module("cachetools")
except ImportError:
    pytest.skip("Cachetools is not installed", allow_module_level=True)