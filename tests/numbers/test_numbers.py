"""Tests for numbers module type aliases.

Tests cover:
- RightAscension: float [0, 360) in degrees
- Declination: float [-90, 90] in degrees
- Redshift: float [0, ∞)
- Distance: float [0, ∞)
"""
import pytest
from pydantic import BaseModel, ValidationError, TypeAdapter

from quasar_typing.numbers import (
    RightAscension,
    Declination,
    Redshift,
    Distance,
)


class TestRightAscension:
    """Test RightAscension validation - float in [0, 360)."""

    def test_ra_accepts_zero(self):
        """RightAscension accepts 0 (inclusive lower bound)."""
        class Model(BaseModel):
            ra: RightAscension

        model = Model(ra=0.0)
        assert model.ra == 0.0

    def test_ra_accepts_positive_values(self):
        """RightAscension accepts various positive values."""
        class Model(BaseModel):
            ra: RightAscension

        for value in [45.0, 90.0, 180.0, 270.0, 359.9, 359.999]:
            model = Model(ra=value)
            assert model.ra == value

    def test_ra_rejects_360(self):
        """RightAscension rejects 360 (exclusive upper bound)."""
        class Model(BaseModel):
            ra: RightAscension

        with pytest.raises(ValidationError) as exc_info:
            Model(ra=360.0)
        assert "less than 360" in str(exc_info.value)

    def test_ra_rejects_greater_than_360(self):
        """RightAscension rejects values > 360."""
        class Model(BaseModel):
            ra: RightAscension

        for value in [360.1, 361.0, 720.0, 1000.0]:
            with pytest.raises(ValidationError):
                Model(ra=value)

    def test_ra_rejects_negative(self):
        """RightAscension rejects negative values."""
        class Model(BaseModel):
            ra: RightAscension

        for value in [-0.1, -45.0, -180.0, -359.0]:
            with pytest.raises(ValidationError) as exc_info:
                Model(ra=value)
            assert "greater than or equal to 0" in str(exc_info.value)

    def test_ra_accepts_int_input(self):
        """RightAscension coerces int to float."""
        class Model(BaseModel):
            ra: RightAscension

        model = Model(ra=90)
        assert model.ra == 90.0
        assert isinstance(model.ra, float)

    def test_ra_accepts_string_input(self):
        """RightAscension coerces numeric string to float."""
        class Model(BaseModel):
            ra: RightAscension

        model = Model(ra="180.5")
        assert model.ra == 180.5

    def test_ra_rejects_non_numeric_string(self):
        """RightAscension rejects non-numeric string."""
        class Model(BaseModel):
            ra: RightAscension

        with pytest.raises(ValidationError):
            Model(ra="not_a_number")

    def test_ra_rejects_none(self):
        """RightAscension rejects None."""
        class Model(BaseModel):
            ra: RightAscension

        with pytest.raises(ValidationError):
            Model(ra=None)

    def test_ra_boundary_near_360(self):
        """RightAscension accepts values arbitrarily close to 360."""
        class Model(BaseModel):
            ra: RightAscension

        for value in [359.9, 359.99, 359.999, 359.9999]:
            model = Model(ra=value)
            assert model.ra == value

    def test_ra_celestial_coordinates(self):
        """RightAscension accepts standard celestial coordinates."""
        class Model(BaseModel):
            ra: RightAscension

        # Standard hour angles in degrees (0-23 hours -> 0-345 degrees)
        standard_ra_values = [
            0.0,     # 0h
            15.0,    # 1h
            90.0,    # 6h
            180.0,   # 12h
            270.0,   # 18h
            337.5,   # 22.5h
        ]
        
        for value in standard_ra_values:
            model = Model(ra=value)
            assert model.ra == value

    def test_ra_in_model_with_other_fields(self):
        """RightAscension works with other fields in model."""
        class Coordinates(BaseModel):
            name: str
            ra: RightAscension
            dec: float

        coord = Coordinates(name="star1", ra=45.5, dec=30.0)
        assert coord.name == "star1"
        assert coord.ra == 45.5

    def test_ra_type_adapter(self):
        """RightAscension validates via TypeAdapter."""
        ta = TypeAdapter(RightAscension)
        
        # Valid
        result = ta.validate_python(123.45)
        assert result == 123.45
        
        # Invalid
        with pytest.raises(ValidationError):
            ta.validate_python(-1.0)


class TestDeclination:
    """Test Declination validation - float in [-90, 90]."""

    def test_dec_accepts_negative_ninety(self):
        """Declination accepts -90 (inclusive lower bound)."""
        class Model(BaseModel):
            dec: Declination

        model = Model(dec=-90.0)
        assert model.dec == -90.0

    def test_dec_accepts_positive_ninety(self):
        """Declination accepts +90 (inclusive upper bound)."""
        class Model(BaseModel):
            dec: Declination

        model = Model(dec=90.0)
        assert model.dec == 90.0

    def test_dec_accepts_zero(self):
        """Declination accepts 0 (celestial equator)."""
        class Model(BaseModel):
            dec: Declination

        model = Model(dec=0.0)
        assert model.dec == 0.0

    def test_dec_accepts_various_values(self):
        """Declination accepts values throughout valid range."""
        class Model(BaseModel):
            dec: Declination

        for value in [-45.0, -30.0, 15.0, 45.0, 60.0, 89.9]:
            model = Model(dec=value)
            assert model.dec == value

    def test_dec_rejects_less_than_minus_90(self):
        """Declination rejects values < -90."""
        class Model(BaseModel):
            dec: Declination

        for value in [-90.1, -91.0, -180.0]:
            with pytest.raises(ValidationError) as exc_info:
                Model(dec=value)
            assert "greater than or equal to -90" in str(exc_info.value)

    def test_dec_rejects_greater_than_90(self):
        """Declination rejects values > 90."""
        class Model(BaseModel):
            dec: Declination

        for value in [90.1, 91.0, 180.0]:
            with pytest.raises(ValidationError) as exc_info:
                Model(dec=value)
            assert "less than or equal to 90" in str(exc_info.value)

    def test_dec_accepts_int_input(self):
        """Declination coerces int to float."""
        class Model(BaseModel):
            dec: Declination

        model = Model(dec=45)
        assert model.dec == 45.0
        assert isinstance(model.dec, float)

    def test_dec_accepts_string_input(self):
        """Declination coerces numeric string to float."""
        class Model(BaseModel):
            dec: Declination

        model = Model(dec="-30.5")
        assert model.dec == -30.5

    def test_dec_rejects_non_numeric_string(self):
        """Declination rejects non-numeric string."""
        class Model(BaseModel):
            dec: Declination

        with pytest.raises(ValidationError):
            Model(dec="not_a_number")

    def test_dec_rejects_none(self):
        """Declination rejects None."""
        class Model(BaseModel):
            dec: Declination

        with pytest.raises(ValidationError):
            Model(dec=None)

    def test_dec_celestial_zones(self):
        """Declination accepts standard celestial zones."""
        class Model(BaseModel):
            dec: Declination

        # North and south poles and equator
        test_values = [-90.0, -60.0, -30.0, 0.0, 30.0, 60.0, 90.0]
        
        for value in test_values:
            model = Model(dec=value)
            assert model.dec == value

    def test_dec_near_limits(self):
        """Declination accepts values arbitrarily close to limits."""
        class Model(BaseModel):
            dec: Declination

        for value in [-89.9, -89.99, 89.9, 89.99]:
            model = Model(dec=value)
            assert model.dec == value

    def test_dec_in_model_with_other_fields(self):
        """Declination works with other fields in model."""
        class Coordinates(BaseModel):
            name: str
            ra: float
            dec: Declination

        coord = Coordinates(name="star1", ra=45.0, dec=-30.5)
        assert coord.name == "star1"
        assert coord.dec == -30.5

    def test_dec_type_adapter(self):
        """Declination validates via TypeAdapter."""
        ta = TypeAdapter(Declination)
        
        # Valid
        result = ta.validate_python(-45.5)
        assert result == -45.5
        
        # Invalid
        with pytest.raises(ValidationError):
            ta.validate_python(91.0)


class TestRedshift:
    """Test Redshift validation - float in [0, ∞)."""

    def test_redshift_accepts_zero(self):
        """Redshift accepts 0 (local universe)."""
        class Model(BaseModel):
            z: Redshift

        model = Model(z=0.0)
        assert model.z == 0.0

    def test_redshift_accepts_positive_values(self):
        """Redshift accepts various positive values."""
        class Model(BaseModel):
            z: Redshift

        for value in [0.001, 0.01, 0.1, 0.5, 1.0, 10.0, 100.0, 1000.0]:
            model = Model(z=value)
            assert model.z == value

    def test_redshift_rejects_negative(self):
        """Redshift rejects negative values."""
        class Model(BaseModel):
            z: Redshift

        for value in [-0.1, -0.01, -1.0, -100.0]:
            with pytest.raises(ValidationError) as exc_info:
                Model(z=value)
            assert "greater than or equal to 0" in str(exc_info.value)

    def test_redshift_accepts_int_input(self):
        """Redshift coerces int to float."""
        class Model(BaseModel):
            z: Redshift

        model = Model(z=1)
        assert model.z == 1.0
        assert isinstance(model.z, float)

    def test_redshift_accepts_string_input(self):
        """Redshift coerces numeric string to float."""
        class Model(BaseModel):
            z: Redshift

        model = Model(z="0.5")
        assert model.z == 0.5

    def test_redshift_rejects_non_numeric_string(self):
        """Redshift rejects non-numeric string."""
        class Model(BaseModel):
            z: Redshift

        with pytest.raises(ValidationError):
            Model(z="not_a_number")

    def test_redshift_rejects_none(self):
        """Redshift rejects None."""
        class Model(BaseModel):
            z: Redshift

        with pytest.raises(ValidationError):
            Model(z=None)

    def test_redshift_accepts_very_small_positive(self):
        """Redshift accepts very small positive values."""
        class Model(BaseModel):
            z: Redshift

        for value in [1e-6, 1e-10, 1e-20]:
            model = Model(z=value)
            assert model.z == value

    def test_redshift_accepts_very_large_values(self):
        """Redshift accepts very large positive values."""
        class Model(BaseModel):
            z: Redshift

        for value in [1e3, 1e6, 1e9]:
            model = Model(z=value)
            assert model.z == value

    def test_redshift_cosmological_distances(self):
        """Redshift accepts typical cosmological redshift values."""
        class Model(BaseModel):
            z: Redshift

        # Typical quasar/galaxy redshifts and CMBR temperature
        test_values = [
            0.0,      # Local universe
            0.01,     # Nearby galaxies (~130 Mly)
            0.1,      # Galaxy clusters
            0.5,      # Typical quasars
            1.0,      # Early universe
            6.5,      # High-z quasars
            1100.0,   # CMBR redshift
        ]
        
        for value in test_values:
            model = Model(z=value)
            assert model.z == value

    def test_redshift_in_model_with_other_fields(self):
        """Redshift works with other fields in model."""
        class Galaxy(BaseModel):
            name: str
            ra: float
            dec: float
            z: Redshift

        galaxy = Galaxy(name="NGC1", ra=45.0, dec=30.0, z=0.5)
        assert galaxy.z == 0.5

    def test_redshift_type_adapter(self):
        """Redshift validates via TypeAdapter."""
        ta = TypeAdapter(Redshift)
        
        # Valid
        result = ta.validate_python(0.75)
        assert result == 0.75
        
        # Invalid
        with pytest.raises(ValidationError):
            ta.validate_python(-0.5)


class TestDistance:
    """Test Distance validation - float in [0, ∞)."""

    def test_distance_accepts_zero(self):
        """Distance accepts 0 (at observer)."""
        class Model(BaseModel):
            dist: Distance

        model = Model(dist=0.0)
        assert model.dist == 0.0

    def test_distance_accepts_positive_values(self):
        """Distance accepts various positive values."""
        class Model(BaseModel):
            dist: Distance

        for value in [0.001, 0.1, 1.0, 10.0, 1000.0, 1e10]:
            model = Model(dist=value)
            assert model.dist == value

    def test_distance_rejects_negative(self):
        """Distance rejects negative values."""
        class Model(BaseModel):
            dist: Distance

        for value in [-0.1, -1.0, -100.0]:
            with pytest.raises(ValidationError) as exc_info:
                Model(dist=value)
            assert "greater than or equal to 0" in str(exc_info.value)

    def test_distance_accepts_int_input(self):
        """Distance coerces int to float."""
        class Model(BaseModel):
            dist: Distance

        model = Model(dist=1000)
        assert model.dist == 1000.0
        assert isinstance(model.dist, float)

    def test_distance_accepts_string_input(self):
        """Distance coerces numeric string to float."""
        class Model(BaseModel):
            dist: Distance

        model = Model(dist="1500.5")
        assert model.dist == 1500.5

    def test_distance_rejects_non_numeric_string(self):
        """Distance rejects non-numeric string."""
        class Model(BaseModel):
            dist: Distance

        with pytest.raises(ValidationError):
            Model(dist="not_a_number")

    def test_distance_rejects_none(self):
        """Distance rejects None."""
        class Model(BaseModel):
            dist: Distance

        with pytest.raises(ValidationError):
            Model(dist=None)

    def test_distance_accepts_very_small_positive(self):
        """Distance accepts very small positive values."""
        class Model(BaseModel):
            dist: Distance

        for value in [1e-6, 1e-10, 1e-20]:
            model = Model(dist=value)
            assert model.dist == value

    def test_distance_accepts_very_large_values(self):
        """Distance accepts very large positive values."""
        class Model(BaseModel):
            dist: Distance

        for value in [1e10, 1e15, 1e20]:
            model = Model(dist=value)
            assert model.dist == value

    def test_distance_astrophysical_scales(self):
        """Distance accepts typical astrophysical distance values (Mpc)."""
        class Model(BaseModel):
            dist: Distance

        # Typical luminosity distances in megaparsecs
        test_values = [
            0.1,      # ~300 kly (nearby galaxies)
            1.0,      # ~3.26 Mly (Local Group)
            10.0,     # ~32.6 Mly (Virgo Cluster)
            100.0,    # ~326 Mly (Coma Cluster)
            1000.0,   # ~3.26 Gly
            10000.0,  # ~32.6 Gly (distant quasars)
        ]
        
        for value in test_values:
            model = Model(dist=value)
            assert model.dist == value

    def test_distance_in_model_with_other_fields(self):
        """Distance works with other fields in model."""
        class Galaxy(BaseModel):
            name: str
            luminosity_distance_mpc: Distance

        galaxy = Galaxy(name="NGC1", luminosity_distance_mpc=1000.5)
        assert galaxy.luminosity_distance_mpc == 1000.5

    def test_distance_type_adapter(self):
        """Distance validates via TypeAdapter."""
        ta = TypeAdapter(Distance)
        
        # Valid
        result = ta.validate_python(500.0)
        assert result == 500.0
        
        # Invalid
        with pytest.raises(ValidationError):
            ta.validate_python(-10.0)


class TestAstronomicalTypesIntegration:
    """Test integration of astronomical types in realistic models."""

    def test_observation_metadata(self):
        """Astronomical types work together in observation model."""
        class Observation(BaseModel):
            ra: RightAscension
            dec: Declination
            redshift: Redshift
            distance_mpc: Distance

        obs = Observation(
            ra=180.0,
            dec=30.0,
            redshift=0.5,
            distance_mpc=2000.0,
        )
        
        assert obs.ra == 180.0
        assert obs.dec == 30.0
        assert obs.redshift == 0.5
        assert obs.distance_mpc == 2000.0

    def test_quasar_catalog_entry(self):
        """Realistic quasar catalog entry with all types."""
        class QuasarEntry(BaseModel):
            name: str
            ra: RightAscension
            dec: Declination
            z: Redshift
            luminosity_distance_mpc: Distance

        quasar = QuasarEntry(
            name="3C273",
            ra=187.2779,
            dec=2.0525,
            z=0.1584,
            luminosity_distance_mpc=740.0,
        )
        
        assert quasar.name == "3C273"
        assert 180 < quasar.ra < 190
        assert -5 < quasar.dec < 5
        assert 0 < quasar.z < 0.2
        assert quasar.luminosity_distance_mpc > 0

    def test_boundary_conditions(self):
        """Test all types at their boundary values."""
        class AstronomicalObject(BaseModel):
            ra: RightAscension
            dec: Declination
            z: Redshift
            dist: Distance

        # South pole observation
        obj1 = AstronomicalObject(ra=0.0, dec=-90.0, z=0.0, dist=0.0)
        assert obj1.ra == 0.0
        assert obj1.dec == -90.0

        # North pole observation
        obj2 = AstronomicalObject(
            ra=359.999, dec=90.0, z=1e10, dist=1e20
        )
        assert obj2.dec == 90.0

    def test_validation_error_clarity(self):
        """Validation errors clearly indicate field and constraint."""
        class Observation(BaseModel):
            ra: RightAscension
            dec: Declination
            z: Redshift
            dist: Distance

        # Invalid RA
        with pytest.raises(ValidationError) as exc_info:
            Observation(ra=400.0, dec=0.0, z=0.0, dist=0.0)
        error_msg = str(exc_info.value)
        assert "ra" in error_msg.lower() or "right" in error_msg.lower()

        # Invalid declination
        with pytest.raises(ValidationError) as exc_info:
            Observation(ra=180.0, dec=100.0, z=0.0, dist=0.0)
        error_msg = str(exc_info.value)
        assert "dec" in error_msg.lower()

    def test_numerical_precision(self):
        """Types preserve numerical precision."""
        class Observation(BaseModel):
            ra: RightAscension
            z: Redshift

        obs = Observation(ra=123.456789, z=0.123456789)
        assert obs.ra == 123.456789
        assert obs.z == 0.123456789
