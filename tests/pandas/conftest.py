"""Shared test fixtures for pandas submodule tests."""

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def simple_dataframe():
    """Simple DataFrame with basic data."""
    return pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4.0, 5.0, 6.0],
        'C': ['x', 'y', 'z']
    })


@pytest.fixture
def empty_dataframe():
    """Empty DataFrame with no rows but has columns."""
    return pd.DataFrame({'A': [], 'B': [], 'C': []})


@pytest.fixture
def numeric_dataframe():
    """DataFrame with only numeric data."""
    return pd.DataFrame({
        'col1': np.array([1, 2, 3, 4, 5]),
        'col2': np.array([10.5, 20.5, 30.5, 40.5, 50.5]),
        'col3': np.array([100, 200, 300, 400, 500])
    })


@pytest.fixture
def multiindex_dataframe():
    """DataFrame with MultiIndex."""
    index = pd.MultiIndex.from_tuples(
        [('a', 1), ('a', 2), ('b', 1), ('b', 2)],
        names=['letter', 'number']
    )
    return pd.DataFrame({
        'value1': [10, 20, 30, 40],
        'value2': [100, 200, 300, 400]
    }, index=index)


@pytest.fixture
def dict_for_dataframe():
    """Dictionary that can be coerced to DataFrame."""
    return {'A': [1, 2, 3], 'B': [4, 5, 6]}


@pytest.fixture
def list_of_lists_for_dataframe():
    """List of lists that can be coerced to DataFrame."""
    return [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


@pytest.fixture
def dict_of_series_for_dataframe():
    """Dictionary of Series that can be coerced to DataFrame."""
    return {
        'A': pd.Series([1, 2, 3]),
        'B': pd.Series([4.0, 5.0, 6.0])
    }
