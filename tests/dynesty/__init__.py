"""Tests for dynesty submodule."""

import importlib

import pytest

try:
    importlib.import_module("dynesty")
except ImportError:
    pytest.skip("Dynesty is not installed", allow_module_level=True)