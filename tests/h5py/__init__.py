"""Tests for h5py module type annotations."""

import importlib

import pytest

try:
    importlib.import_module("h5py")
except ImportError:
    pytest.skip("H5py is not installed", allow_module_level=True)