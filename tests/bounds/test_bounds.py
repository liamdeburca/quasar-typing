import pytest
from pydantic import BaseModel, ValidationError
from quasar_typing.bounds import AstropyBounds, CoordBounds


class TestAstropyBounds:
    """Test AstropyBounds validation for astropy bounds"""

    def test_valid_bounds_both_float(self):
        """Test valid bounds with two float values"""
        class Model(BaseModel):
            bounds: AstropyBounds

        m = Model(bounds=(1.0, 2.0))
        assert m.bounds == (1.0, 2.0)

    def test_valid_bounds_lower_none(self):
        """Test valid bounds with lower value as None"""
        class Model(BaseModel):
            bounds: AstropyBounds

        m = Model(bounds=(None, 2.0))
        assert m.bounds == (None, 2.0)

    def test_valid_bounds_upper_none(self):
        """Test valid bounds with upper value as None"""
        class Model(BaseModel):
            bounds: AstropyBounds

        m = Model(bounds=(1.0, None))
        assert m.bounds == (1.0, None)

    def test_both_none_fails(self):
        """Test that bounds with both None values fail"""
        class Model(BaseModel):
            bounds: AstropyBounds

        with pytest.raises(ValidationError) as exc_info:
            Model(bounds=(None, None))
        assert "cannot contain only 'None' values" in str(exc_info.value)

    def test_not_tuple_fails(self):
        """Test that non-tuple input fails"""
        class Model(BaseModel):
            bounds: AstropyBounds

        with pytest.raises(ValidationError) as exc_info:
            Model(bounds=[1.0, 2.0])
        assert "must be a 'tuple'" in str(exc_info.value)

    def test_single_element_fails(self):
        """Test that single element tuple fails"""
        class Model(BaseModel):
            bounds: AstropyBounds

        with pytest.raises(ValidationError) as exc_info:
            Model(bounds=(1.0,))
        assert "contain 2 values" in str(exc_info.value)

    def test_three_elements_fails(self):
        """Test that three element tuple fails"""
        class Model(BaseModel):
            bounds: AstropyBounds

        with pytest.raises(ValidationError) as exc_info:
            Model(bounds=(1.0, 2.0, 3.0))
        assert "contain 2 values" in str(exc_info.value)

    def test_non_decreasing_bounds_fails(self):
        """Test that non-increasing bounds fail"""
        class Model(BaseModel):
            bounds: AstropyBounds

        with pytest.raises(ValidationError) as exc_info:
            Model(bounds=(2.0, 1.0))
        assert "must be 'increasing'" in str(exc_info.value)

    def test_equal_bounds_fails(self):
        """Test that equal bounds fail"""
        class Model(BaseModel):
            bounds: AstropyBounds

        with pytest.raises(ValidationError) as exc_info:
            Model(bounds=(1.0, 1.0))
        assert "must be 'increasing'" in str(exc_info.value)

    def test_non_float_element_fails(self):
        """Test that non-float element fails"""
        class Model(BaseModel):
            bounds: AstropyBounds

        with pytest.raises(ValidationError) as exc_info:
            Model(bounds=(1, 2.0))
        assert "must be of type 'float' or 'None'" in str(exc_info.value)

    def test_non_float_string_fails(self):
        """Test that string element fails"""
        class Model(BaseModel):
            bounds: AstropyBounds

        with pytest.raises(ValidationError) as exc_info:
            Model(bounds=("1.0", 2.0))
        assert "must be of type 'float' or 'None'" in str(exc_info.value)

    def test_large_negative_to_positive(self):
        """Test bounds spanning negative to positive values"""
        class Model(BaseModel):
            bounds: AstropyBounds

        m = Model(bounds=(-100.5, 100.5))
        assert m.bounds == (-100.5, 100.5)

    def test_small_difference_bounds(self):
        """Test bounds with very small difference"""
        class Model(BaseModel):
            bounds: AstropyBounds

        m = Model(bounds=(1.0, 1.000001))
        assert m.bounds == (1.0, 1.000001)

    def test_zero_included_in_bounds(self):
        """Test bounds that include zero"""
        class Model(BaseModel):
            bounds: AstropyBounds

        m = Model(bounds=(-1.5, 2.5))
        assert m.bounds == (-1.5, 2.5)

    def test_none_and_negative_bound(self):
        """Test None with negative bound"""
        class Model(BaseModel):
            bounds: AstropyBounds

        m = Model(bounds=(None, -1.0))
        assert m.bounds == (None, -1.0)

    def test_none_skip_ordering_check(self):
        """Test that ordering is only checked when both values are not None"""
        class Model(BaseModel):
            bounds: AstropyBounds

        # When one is None, ordering check is skipped
        m = Model(bounds=(100.0, None))
        assert m.bounds == (100.0, None)


class TestCoordBounds:
    """Test CoordBounds validation for coordinate bounds"""

    def test_valid_bounds_both_float(self):
        """Test valid bounds with two float values"""
        class Model(BaseModel):
            bounds: CoordBounds

        m = Model(bounds=(1.0, 2.0))
        assert m.bounds == (1.0, 2.0)

    def test_valid_bounds_int_input(self):
        """Test that int input is converted to float"""
        class Model(BaseModel):
            bounds: CoordBounds

        m = Model(bounds=(1, 2))
        assert m.bounds == (1.0, 2.0)
        assert all(isinstance(v, float) for v in m.bounds)

    def test_valid_bounds_mixed_int_float(self):
        """Test that mixed int and float input works"""
        class Model(BaseModel):
            bounds: CoordBounds

        m = Model(bounds=(1, 2.0))
        assert m.bounds == (1.0, 2.0)

    def test_not_tuple_fails(self):
        """Test that non-tuple input fails"""
        class Model(BaseModel):
            bounds: CoordBounds

        with pytest.raises(ValidationError) as exc_info:
            Model(bounds=[1.0, 2.0])
        assert "must be a 'tuple'" in str(exc_info.value)

    def test_single_element_fails(self):
        """Test that single element tuple fails"""
        class Model(BaseModel):
            bounds: CoordBounds

        with pytest.raises(ValidationError) as exc_info:
            Model(bounds=(1.0,))
        assert "contain 2 values" in str(exc_info.value)

    def test_three_elements_fails(self):
        """Test that three element tuple fails"""
        class Model(BaseModel):
            bounds: CoordBounds

        with pytest.raises(ValidationError) as exc_info:
            Model(bounds=(1.0, 2.0, 3.0))
        assert "contain 2 values" in str(exc_info.value)

    def test_non_decreasing_bounds_fails(self):
        """Test that non-increasing bounds fail"""
        class Model(BaseModel):
            bounds: CoordBounds

        with pytest.raises(ValidationError) as exc_info:
            Model(bounds=(2.0, 1.0))
        assert "must be 'increasing'" in str(exc_info.value)

    def test_equal_bounds_fails(self):
        """Test that equal bounds fail"""
        class Model(BaseModel):
            bounds: CoordBounds

        with pytest.raises(ValidationError) as exc_info:
            Model(bounds=(1.0, 1.0))
        assert "must be 'increasing'" in str(exc_info.value)

    def test_non_numeric_element_fails(self):
        """Test that non-numeric element fails"""
        class Model(BaseModel):
            bounds: CoordBounds

        with pytest.raises(ValidationError) as exc_info:
            Model(bounds=(1.0, "2.0"))
        assert "must be of type 'float'" in str(exc_info.value)

    def test_none_element_fails(self):
        """Test that None element fails for CoordBounds"""
        class Model(BaseModel):
            bounds: CoordBounds

        with pytest.raises(ValidationError) as exc_info:
            Model(bounds=(None, 2.0))
        assert "must be of type 'float'" in str(exc_info.value)

    def test_large_negative_to_positive(self):
        """Test bounds spanning negative to positive values"""
        class Model(BaseModel):
            bounds: CoordBounds

        m = Model(bounds=(-100.5, 100.5))
        assert m.bounds == (-100.5, 100.5)

    def test_small_difference_bounds(self):
        """Test bounds with very small difference"""
        class Model(BaseModel):
            bounds: CoordBounds

        m = Model(bounds=(1.0, 1.000001))
        assert m.bounds == (1.0, 1.000001)

    def test_zero_included_in_bounds(self):
        """Test bounds that include zero"""
        class Model(BaseModel):
            bounds: CoordBounds

        m = Model(bounds=(-1.5, 2.5))
        assert m.bounds == (-1.5, 2.5)

    def test_negative_bounds(self):
        """Test bounds with both negative values"""
        class Model(BaseModel):
            bounds: CoordBounds

        m = Model(bounds=(-100.0, -10.0))
        assert m.bounds == (-100.0, -10.0)

    def test_zero_lower_bound(self):
        """Test bounds with zero as lower bound"""
        class Model(BaseModel):
            bounds: CoordBounds

        m = Model(bounds=(0.0, 10.0))
        assert m.bounds == (0.0, 10.0)

    def test_scientific_notation(self):
        """Test bounds with scientific notation"""
        class Model(BaseModel):
            bounds: CoordBounds

        m = Model(bounds=(1e-5, 1e-4))
        assert m.bounds == (1e-5, 1e-4)


class TestBoundsEdgeCases:
    """Test edge cases and special scenarios"""

    def test_astropy_bounds_very_large_range(self):
        """Test AstropyBounds with very large range"""
        class Model(BaseModel):
            bounds: AstropyBounds

        m = Model(bounds=(-1e10, 1e10))
        assert m.bounds == (-1e10, 1e10)

    def test_coord_bounds_very_large_range(self):
        """Test CoordBounds with very large range"""
        class Model(BaseModel):
            bounds: CoordBounds

        m = Model(bounds=(-1e10, 1e10))
        assert m.bounds == (-1e10, 1e10)

    def test_astropy_bounds_float_precision(self):
        """Test AstropyBounds preserves float precision"""
        class Model(BaseModel):
            bounds: AstropyBounds

        value = (1.23456789, 2.98765432)
        m = Model(bounds=value)
        assert m.bounds[0] == value[0]
        assert m.bounds[1] == value[1]

    def test_coord_bounds_int_to_float_conversion(self):
        """Test CoordBounds properly converts int to float"""
        class Model(BaseModel):
            bounds: CoordBounds

        m = Model(bounds=(1, 2))
        assert isinstance(m.bounds[0], float)
        assert isinstance(m.bounds[1], float)
        assert m.bounds == (1.0, 2.0)

    def test_astropy_bounds_both_none_explicit(self):
        """Test explicit None for both values in AstropyBounds"""
        class Model(BaseModel):
            bounds: AstropyBounds

        with pytest.raises(ValidationError):
            Model(bounds=(None, None))

    def test_bounds_tuple_immutability(self):
        """Test that returned bounds are tuple (immutable)"""
        class Model(BaseModel):
            bounds: CoordBounds

        m = Model(bounds=(1.0, 2.0))
        assert isinstance(m.bounds, tuple)
        with pytest.raises(TypeError):
            m.bounds[0] = 3.0
