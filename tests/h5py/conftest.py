"""Pytest configuration for h5py tests."""
import pytest
import tempfile
import h5py


@pytest.fixture
def h5_file():
    """Create a temporary HDF5 file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.h5', delete=False) as tmp:
        tmp_path = tmp.name
    
    # Create a simple HDF5 file
    with h5py.File(tmp_path, 'w') as f:
        f.create_group('group1')
        f.create_dataset('dataset1', data=[1, 2, 3, 4, 5])
        f.attrs['file_attr'] = 'test_file'
    
    yield tmp_path
    
    # Cleanup
    import os
    if os.path.exists(tmp_path):
        os.remove(tmp_path)


@pytest.fixture
def h5_file_object(h5_file):
    """Open an HDF5 file and return file object."""
    f = h5py.File(h5_file, 'r')
    yield f
    f.close()


@pytest.fixture
def h5_group(h5_file_object):
    """Get a group from opened HDF5 file."""
    return h5_file_object['group1']


@pytest.fixture
def h5_dataset(h5_file_object):
    """Get a dataset from opened HDF5 file."""
    return h5_file_object['dataset1']
