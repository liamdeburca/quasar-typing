"""Tests for emcee submodule."""

import importlib

import pytest

try:
    importlib.import_module("emcee")
except ImportError:
    pytest.skip("Emcee is not installed", allow_module_level=True)