import shutil
import tempfile
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def testdata_dir() -> Path:
    """Create a temporary directory with sample files for pathlib tests.

    Yields the Path to the directory and removes it after the test session.
    """
    td = Path(tempfile.mkdtemp(prefix="quasar_pathlib_test_"))

    # create directories
    (td / "dir1").mkdir()
    (td / "dir2").mkdir()

    # create files with various extensions
    files = [
        "sample.csv",
        "sample.json",
        "sample.asc",
        "sample.fits",
        "sample.pkl",
        "sample.yaml",
        "sample.yml",
        "sample.toml",
        "sample.toon",
        "sample.h5",
        "sample.hdf5",
        "sample.log",
    ]

    for name in files:
        p = td / name
        p.write_text(f"contents of {name}\n")

    yield td

    # cleanup
    try:
        shutil.rmtree(td)
    except Exception:
        pass
