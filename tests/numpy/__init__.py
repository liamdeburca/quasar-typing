import importlib

import pytest

try:
    importlib.import_module("numpy")
except ImportError:
    pytest.skip("Numpy is not installed", allow_module_level=True)