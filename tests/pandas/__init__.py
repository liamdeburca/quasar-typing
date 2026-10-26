"""Tests for pandas submodule."""

import importlib

import pytest

try:
    importlib.import_module("pandas")
except ImportError:
    pytest.skip("Pandas is not installed", allow_module_level=True)