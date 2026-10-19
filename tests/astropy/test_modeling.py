import astropy.units as u
import pytest
from astropy.coordinates import SkyCoord
from astropy.io.fits import BinTableHDU, HDUList, ImageHDU, PrimaryHDU
from astropy.modeling import (
    CompoundModel,
    Fittable1DModel,
    Model,
    Parameter,
)
from astropy.modeling.models import Gaussian1D, Lorentz1D, Polynomial1D
from astropy.table import QTable, Table
from pydantic import TypeAdapter, ValidationError
from pydantic_core.core_schema import no_info_plain_validator_function

from quasar_typing.astropy import (
    BinTableHDUType,
    CompoundModelType,
    Fittable1DModelType,
    HDUListType,
    ImageHDUType,
    ModelType,
    ParameterType,
    PrimaryHDUType,
    QTableType,
    QuantityType,
    SkyCoordType,
    TableType,
    UnitType,
)
from quasar_typing.utils import isinstance_func


class ValidatedGaussian1D(Gaussian1D):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(Gaussian1D)
        )


class ValidatedLorentz1D(Lorentz1D):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(Lorentz1D)
        )


class ValidatedPolynomial1D(Polynomial1D):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(Polynomial1D)
        )


class TestModelType:
    """Test ModelType validation."""

    def test_positive_with_model(self, gaussian_model):
        """Valid Model should pass validation."""
        ta = TypeAdapter(ModelType)
        result = ta.validate_python(gaussian_model)
        assert isinstance(result, Model)
        assert isinstance(result, Gaussian1D)

    def test_positive_with_polynomial(self, polynomial_model):
        """Valid Polynomial1D model should pass validation."""
        ta = TypeAdapter(ModelType)
        result = ta.validate_python(polynomial_model)
        assert isinstance(result, Model)

    def test_negative_with_non_model(self):
        """Non-Model objects should fail validation."""
        ta = TypeAdapter(ModelType)
        with pytest.raises(ValidationError):
            ta.validate_python("not a model")


class TestFittable1DModelType:
    """Test Fittable1DModelType validation."""

    def test_positive_with_gaussian(self, gaussian_model):
        """Valid Fittable1DModel should pass validation."""
        ta = TypeAdapter(Fittable1DModelType)
        result = ta.validate_python(gaussian_model)
        assert isinstance(result, Fittable1DModel)

    def test_positive_with_lorentz(self, lorentz_model):
        """Valid Lorentz1D model should pass validation."""
        ta = TypeAdapter(Fittable1DModelType)
        result = ta.validate_python(lorentz_model)
        assert isinstance(result, Fittable1DModel)

    def test_negative_with_polynomial(self, polynomial_model):
        """Polynomial1D is not Fittable1DModel, should fail."""
        ta = TypeAdapter(Fittable1DModelType)
        with pytest.raises(ValidationError):
            ta.validate_python(polynomial_model)


class TestParameterType:
    """Test ParameterType validation."""

    def test_positive_with_parameter(self, gaussian_model):
        """Valid Parameter should pass validation."""
        ta = TypeAdapter(ParameterType)
        param = gaussian_model.amplitude
        result = ta.validate_python(param)
        assert isinstance(result, Parameter)

    def test_negative_with_non_parameter(self):
        """Non-Parameter objects should fail validation."""
        ta = TypeAdapter(ParameterType)
        with pytest.raises(ValidationError):
            ta.validate_python("not a parameter")


class TestCompoundModelType:
    """Test CompoundModelType validation."""

    def test_positive_basic(self, compound_model_gaussian_poly):
        """Valid CompoundModel should pass validation."""
        ta = TypeAdapter(CompoundModelType)
        result = ta.validate_python(compound_model_gaussian_poly)
        assert isinstance(result, CompoundModel)

    def test_positive_with_different_compound(self, compound_model_lorentz_gaussian):
        """Different valid CompoundModel should pass validation."""
        ta = TypeAdapter(CompoundModelType)
        result = ta.validate_python(compound_model_lorentz_gaussian)
        assert isinstance(result, CompoundModel)

    def test_negative_with_single_model(self, gaussian_model):
        """Single models should fail (they are not CompoundModels)."""
        ta = TypeAdapter(CompoundModelType)
        with pytest.raises(ValidationError):
            ta.validate_python(gaussian_model)

    def test_negative_with_non_model(self):
        """Non-CompoundModel objects should fail validation."""
        ta = TypeAdapter(CompoundModelType)
        with pytest.raises(ValidationError):
            ta.validate_python("not a compound model")

    def test_typed_compound_model_single_type(self, gaussian_model):
        """CompoundModelType[Gaussian1D] should validate submodel types."""
        # Create a compound model with only Gaussian submodels
        compound = gaussian_model + Gaussian1D(amplitude=2.0)
        
        # Use tuple unpacking since we can't use multi-arg syntax
        GaussianCompoundType = CompoundModelType[ValidatedGaussian1D]
        ta = TypeAdapter(GaussianCompoundType)
        result = ta.validate_python(compound)
        assert isinstance(result, CompoundModel)

    def test_typed_compound_model_wrong_subtype(
        self, gaussian_model, lorentz_model
    ):
        """CompoundModelType[Gaussian1D] should reject non-Gaussian submodels."""
        # Create a compound model with a Lorentz model
        compound = gaussian_model + lorentz_model        
        GaussianCompoundType = CompoundModelType[ValidatedGaussian1D]
        ta = TypeAdapter(GaussianCompoundType)
        with pytest.raises(ValidationError):
            ta.validate_python(compound)

    def test_wrongly_typed_compound_model_raises_type_error(self):
        with pytest.raises(TypeError):
            CompoundModelType[Gaussian1D]

        with pytest.raises(TypeError):
            CompoundModelType[Lorentz1D]
        

class TestHDUListType:
    """Test HDUListType validation."""

    def test_positive(self, hdulist):
        """Valid HDUList should pass validation."""
        ta = TypeAdapter(HDUListType)
        result = ta.validate_python(hdulist)
        assert isinstance(result, HDUList)

    def test_negative(self):
        """Non-HDUList should fail validation."""
        ta = TypeAdapter(HDUListType)
        with pytest.raises(ValidationError):
            ta.validate_python("not an hdulist")


class TestPrimaryHDUType:
    """Test PrimaryHDUType validation."""

    def test_positive(self, primary_hdu):
        """Valid PrimaryHDU should pass validation."""
        ta = TypeAdapter(PrimaryHDUType)
        result = ta.validate_python(primary_hdu)
        assert isinstance(result, PrimaryHDU)

    def test_negative(self, image_hdu):
        """ImageHDU should fail PrimaryHDU validation."""
        ta = TypeAdapter(PrimaryHDUType)
        with pytest.raises(ValidationError):
            ta.validate_python(image_hdu)


class TestImageHDUType:
    """Test ImageHDUType validation."""

    def test_positive(self, image_hdu):
        """Valid ImageHDU should pass validation."""
        ta = TypeAdapter(ImageHDUType)
        result = ta.validate_python(image_hdu)
        assert isinstance(result, ImageHDU)

    def test_negative(self, primary_hdu):
        """PrimaryHDU should fail ImageHDU validation."""
        ta = TypeAdapter(ImageHDUType)
        with pytest.raises(ValidationError):
            ta.validate_python(primary_hdu)


class TestBinTableHDUType:
    """Test BinTableHDUType validation."""

    def test_positive(self, bintable_hdu):
        """Valid BinTableHDU should pass validation."""
        ta = TypeAdapter(BinTableHDUType)
        result = ta.validate_python(bintable_hdu)
        assert isinstance(result, BinTableHDU)

    def test_negative(self, image_hdu):
        """ImageHDU should fail BinTableHDU validation."""
        ta = TypeAdapter(BinTableHDUType)
        with pytest.raises(ValidationError):
            ta.validate_python(image_hdu)


class TestTableType:
    """Test TableType validation."""

    def test_positive(self, simple_table):
        """Valid Table should pass validation."""
        ta = TypeAdapter(TableType)
        result = ta.validate_python(simple_table)
        assert isinstance(result, Table)

    def test_negative(self):
        """Non-Table should fail validation."""
        ta = TypeAdapter(TableType)
        with pytest.raises(ValidationError):
            ta.validate_python([1, 2, 3])


class TestQTableType:
    """Test QTableType validation."""

    def test_positive(self, quantity_table):
        """Valid QTable should pass validation."""
        ta = TypeAdapter(QTableType)
        result = ta.validate_python(quantity_table)
        assert isinstance(result, QTable)

    def test_negative(self):
        """Non-QTable should fail validation."""
        ta = TypeAdapter(QTableType)
        with pytest.raises(ValidationError):
            ta.validate_python([1, 2, 3])


class TestSkyCoordType:
    """Test SkyCoordType validation."""

    def test_positive(self, sky_coord):
        """Valid SkyCoord should pass validation."""
        ta = TypeAdapter(SkyCoordType)
        result = ta.validate_python(sky_coord)
        assert isinstance(result, SkyCoord)

    def test_negative(self):
        """Non-SkyCoord should fail validation."""
        ta = TypeAdapter(SkyCoordType)
        with pytest.raises(ValidationError):
            ta.validate_python("not a skycoord")


class TestQuantityType:
    """Test QuantityType validation."""

    def test_positive(self, quantity_table):
        """Valid Quantity should pass validation."""
        ta = TypeAdapter(QuantityType)
        quantity = 1.0 * u.meter
        result = ta.validate_python(quantity)
        assert hasattr(result, 'unit')

    def test_negative(self):
        """Non-Quantity should fail validation."""
        ta = TypeAdapter(QuantityType)
        with pytest.raises(ValidationError):
            ta.validate_python("not a quantity")


class TestUnitType:
    """Test UnitType validation."""

    def test_positive(self):
        """Valid Unit should pass validation."""
        ta = TypeAdapter(UnitType)
        result = ta.validate_python("meter")
        assert result == u.meter

    def test_positive_with_unit_object(self):
        """Valid Unit object should pass validation."""
        ta = TypeAdapter(UnitType)
        result = ta.validate_python(u.km)
        assert result == u.km

    def test_negative(self):
        """Invalid Unit string should fail validation."""
        ta = TypeAdapter(UnitType)
        with pytest.raises(ValidationError):
            # Use a string with invalid syntax
            ta.validate_python("meter/second/invalid")
