"""Tests for scipy module types and validators."""

import importlib

import pytest

try:
    importlib.import_module("scipy")
except ImportError:
    pytest.skip("Scipy is not installed", allow_module_level=True)