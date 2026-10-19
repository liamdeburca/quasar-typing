import astropy.units as u
import numpy as np
import pytest
from astropy.coordinates import SkyCoord
from astropy.io.fits import BinTableHDU, HDUList, ImageHDU, PrimaryHDU
from astropy.modeling.models import Gaussian1D, Lorentz1D, Polynomial1D
from astropy.table import QTable, Table


@pytest.fixture
def gaussian_model():
    """Create a simple Gaussian1D model."""
    return Gaussian1D(amplitude=1.0, mean=0.0, stddev=1.0)


@pytest.fixture
def lorentz_model():
    """Create a simple Lorentz1D model."""
    return Lorentz1D(amplitude=1.0, x_0=0.0, fwhm=1.0)


@pytest.fixture
def polynomial_model():
    """Create a simple Polynomial1D model."""
    return Polynomial1D(degree=2, c0=1.0, c1=2.0, c2=3.0)


@pytest.fixture
def compound_model_gaussian_poly(gaussian_model, polynomial_model):
    """Create a compound model from Gaussian and Polynomial."""
    return gaussian_model + polynomial_model


@pytest.fixture
def compound_model_lorentz_gaussian(lorentz_model, gaussian_model):
    """Create a compound model from Lorentz and Gaussian."""
    return lorentz_model | gaussian_model


@pytest.fixture
def primary_hdu():
    """Create a simple PrimaryHDU."""
    data = np.arange(100).reshape(10, 10)
    return PrimaryHDU(data=data)


@pytest.fixture
def image_hdu():
    """Create a simple ImageHDU."""
    data = np.arange(100).reshape(10, 10)
    return ImageHDU(data=data, name='IMAGE')


@pytest.fixture
def bintable_hdu():
    """Create a simple BinTableHDU."""
    col1 = np.array([1, 2, 3])
    col2 = np.array([1.0, 2.0, 3.0])
    from astropy.io.fits import Column
    cols = [
        Column(name='col1', format='J', array=col1),
        Column(name='col2', format='D', array=col2),
    ]
    return BinTableHDU.from_columns(cols)


@pytest.fixture
def hdulist(primary_hdu, image_hdu):
    """Create a simple HDUList."""
    return HDUList([primary_hdu, image_hdu])


@pytest.fixture
def simple_table():
    """Create a simple Table."""
    return Table({
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'height': [170, 180, 175],
    })


@pytest.fixture
def quantity_table():
    """Create a QTable with units."""
    return QTable({
        'distance': [1.0, 2.0, 3.0] * u.pc,
        'velocity': [100, 200, 300] * u.km / u.s,
    })


@pytest.fixture
def sky_coord():
    """Create a simple SkyCoord."""
    return SkyCoord(ra=10.0*u.deg, dec=20.0*u.deg)
