"""Tests for misc module validators.

Tests cover:
- WindowSize: PositiveInt with odd value validation
- PolynomialOrder: NonNegativeInt for polynomial degrees
"""
import pytest
from pydantic import BaseModel, ValidationError

from quasar_typing.misc import PolynomialOrder, WindowSize


class TestWindowSize:
    """Test WindowSize validation - PositiveInt that must be odd."""

    def test_window_size_accepts_odd_positive_int(self):
        """WindowSize accepts positive odd integers."""
        class Model(BaseModel):
            window_size: WindowSize

        # Test various odd numbers
        for value in [1, 3, 5, 7, 11, 99, 101, 1001]:
            model = Model(window_size=value)
            assert model.window_size == value

    def test_window_size_rejects_even_positive_int(self):
        """WindowSize rejects even positive integers."""
        class Model(BaseModel):
            window_size: WindowSize

        # Test various even numbers
        for value in [2, 4, 6, 8, 10, 100, 1000]:
            with pytest.raises(ValidationError) as exc_info:
                Model(window_size=value)
            assert "must be odd" in str(exc_info.value)

    def test_window_size_rejects_zero(self):
        """WindowSize rejects zero (not positive)."""
        class Model(BaseModel):
            window_size: WindowSize

        with pytest.raises(ValidationError) as exc_info:
            Model(window_size=0)
        # Could be caught by PositiveInt or by odd validator
        assert "greater than 0" in str(exc_info.value) or "positive" in str(exc_info.value).lower()

    def test_window_size_rejects_negative_odd(self):
        """WindowSize rejects negative odd integers."""
        class Model(BaseModel):
            window_size: WindowSize

        for value in [-1, -3, -5, -99]:
            with pytest.raises(ValidationError) as exc_info:
                Model(window_size=value)
            # Could be caught by PositiveInt or by odd validator
            error_msg = str(exc_info.value).lower()
            assert "positive" in error_msg or "greater than 0" in error_msg or "odd" in error_msg

    def test_window_size_rejects_negative_even(self):
        """WindowSize rejects negative even integers."""
        class Model(BaseModel):
            window_size: WindowSize

        for value in [-2, -4, -10, -100]:
            with pytest.raises(ValidationError):
                Model(window_size=value)

    def test_window_size_rejects_float(self):
        """WindowSize rejects float values."""
        class Model(BaseModel):
            window_size: WindowSize

        with pytest.raises(ValidationError):
            Model(window_size=3.5)

    def test_window_size_rejects_non_numeric_string(self):
        """WindowSize rejects non-numeric string values."""
        class Model(BaseModel):
            window_size: WindowSize

        with pytest.raises(ValidationError):
            Model(window_size="not_a_number")

    def test_window_size_rejects_none(self):
        """WindowSize rejects None."""
        class Model(BaseModel):
            window_size: WindowSize

        with pytest.raises(ValidationError):
            Model(window_size=None)

    def test_window_size_coerces_from_int_string(self):
        """WindowSize coerces numeric strings to int and validates."""
        class Model(BaseModel):
            window_size: WindowSize

        # Pydantic can coerce numeric strings
        model = Model(window_size="5")
        assert model.window_size == 5

    def test_window_size_boundary_values(self):
        """WindowSize accepts boundary odd values."""
        class Model(BaseModel):
            window_size: WindowSize

        # Test very small odd
        model1 = Model(window_size=1)
        assert model1.window_size == 1

        # Test large odd
        model2 = Model(window_size=9999)
        assert model2.window_size == 9999

    def test_window_size_in_model_with_other_fields(self):
        """WindowSize works with other fields in model."""
        class Config(BaseModel):
            name: str
            window_size: WindowSize
            threshold: float

        config = Config(name="test", window_size=7, threshold=0.5)
        assert config.name == "test"
        assert config.window_size == 7
        assert config.threshold == 0.5

    def test_window_size_multiple_fields(self):
        """Multiple WindowSize fields validate independently."""
        class Model(BaseModel):
            size1: WindowSize
            size2: WindowSize

        model = Model(size1=3, size2=11)
        assert model.size1 == 3
        assert model.size2 == 11

    def test_window_size_validation_error_message(self):
        """WindowSize validation error includes clear message."""
        class Model(BaseModel):
            window_size: WindowSize

        with pytest.raises(ValidationError) as exc_info:
            Model(window_size=4)
        
        error = str(exc_info.value)
        assert "window_size" in error.lower() or "must be odd" in error

    def test_window_size_odd_validation_order(self):
        """WindowSize validates odd after positive."""
        class Model(BaseModel):
            window_size: WindowSize

        # -1 fails on PositiveInt constraint
        with pytest.raises(ValidationError):
            Model(window_size=-1)

        # 2 fails on odd constraint
        with pytest.raises(ValidationError) as exc_info:
            Model(window_size=2)
        assert "odd" in str(exc_info.value)


class TestPolynomialOrder:
    """Test PolynomialOrder validation - PositiveInt for polynomial degrees."""

    def test_polynomial_order_accepts_positive_int(self):
        """PolynomialOrder accepts positive integers."""
        class Model(BaseModel):
            order: PolynomialOrder

        # Test various positive values
        for value in [0, 1, 2, 3, 5, 10, 100, 1000]:
            model = Model(order=value)
            assert model.order == value

    def test_polynomial_order_accepts_even_and_odd(self):
        """PolynomialOrder accepts both even and odd (no odd constraint)."""
        class Model(BaseModel):
            order: PolynomialOrder

        # Even
        model1 = Model(order=4)
        assert model1.order == 4

        # Odd
        model2 = Model(order=5)
        assert model2.order == 5

    def test_polynomial_order_rejects_negative(self):
        """PolynomialOrder rejects negative values."""
        class Model(BaseModel):
            order: PolynomialOrder

        for value in [-1, -2, -5, -100]:
            with pytest.raises(ValidationError):
                Model(order=value)

    def test_polynomial_order_rejects_float(self):
        """PolynomialOrder rejects float values."""
        class Model(BaseModel):
            order: PolynomialOrder

        with pytest.raises(ValidationError):
            Model(order=2.5)

    def test_polynomial_order_rejects_none(self):
        """PolynomialOrder rejects None."""
        class Model(BaseModel):
            order: PolynomialOrder

        with pytest.raises(ValidationError):
            Model(order=None)

    def test_polynomial_order_coerces_from_string(self):
        """PolynomialOrder coerces numeric strings to int."""
        class Model(BaseModel):
            order: PolynomialOrder

        model = Model(order="3")
        assert model.order == 3

    def test_polynomial_order_boundary_values(self):
        """PolynomialOrder accepts boundary values."""
        class Model(BaseModel):
            order: PolynomialOrder

        # Minimum positive
        model1 = Model(order=1)
        assert model1.order == 1

        # Large value
        model2 = Model(order=100000)
        assert model2.order == 100000

    def test_polynomial_order_in_model(self):
        """PolynomialOrder works with other fields."""
        class Config(BaseModel):
            name: str
            order: PolynomialOrder
            coefficients: list[float]

        config = Config(
            name="linear",
            order=1,
            coefficients=[1.0, 2.0],
        )
        assert config.order == 1

    def test_polynomial_order_multiple_fields(self):
        """Multiple PolynomialOrder fields validate independently."""
        class Model(BaseModel):
            linear_order: PolynomialOrder
            quadratic_order: PolynomialOrder

        model = Model(linear_order=1, quadratic_order=2)
        assert model.linear_order == 1
        assert model.quadratic_order == 2

    def test_polynomial_order_difference_from_window_size(self):
        """PolynomialOrder and WindowSize differ only in odd constraint."""
        from quasar_typing.misc import WindowSize
        
        class Model(BaseModel):
            window_size: WindowSize
            poly_order: PolynomialOrder

        # poly_order=4 works, but window_size=4 would fail
        model = Model(poly_order=4, window_size=5)
        assert model.poly_order == 4
        assert model.window_size == 5

        # Verify window_size rejects even
        with pytest.raises(ValidationError):
            Model(poly_order=4, window_size=4)


class TestWindowSizeAndPolynomialOrderInteraction:
    """Test interaction between WindowSize and PolynomialOrder."""

    def test_combined_model(self):
        """Model with both WindowSize and PolynomialOrder."""
        class FilterConfig(BaseModel):
            window_size: WindowSize
            polynomial_order: PolynomialOrder
            name: str

        config = FilterConfig(
            window_size=5,
            polynomial_order=2,
            name="savitzky_golay",
        )
        assert config.window_size == 5
        assert config.polynomial_order == 2
        assert config.name == "savitzky_golay"

    def test_window_size_must_be_odd_poly_order_any(self):
        """WindowSize must be odd, but PolynomialOrder can be anything."""
        class Config(BaseModel):
            window_size: WindowSize
            polynomial_order: PolynomialOrder

        # window_size=3 (odd), poly_order=2 (even) - both valid
        config = Config(window_size=3, polynomial_order=2)
        assert config.window_size == 3
        assert config.polynomial_order == 2

    def test_typical_filter_config(self):
        """Typical Savitzky-Golay filter configuration."""
        class SavitzkyGolayFilter(BaseModel):
            window_size: WindowSize  # Must be odd
            polynomial_order: PolynomialOrder  # Typically less than window_size

        # Valid: window=7, order=3
        config = SavitzkyGolayFilter(window_size=7, polynomial_order=3)
        assert config.window_size == 7
        assert config.polynomial_order == 3

        # Invalid: window=6 (even)
        with pytest.raises(ValidationError):
            SavitzkyGolayFilter(window_size=6, polynomial_order=3)

    def test_edge_case_same_values(self):
        """Both can have same numeric value if within constraints."""
        class Model(BaseModel):
            window_size: WindowSize
            polynomial_order: PolynomialOrder

        # Both 5: window_size accepts (odd), poly_order accepts (any positive)
        model = Model(window_size=5, polynomial_order=5)
        assert model.window_size == 5
        assert model.polynomial_order == 5


class TestMiscEdgeCases:
    """Test edge cases for misc module types."""

    def test_large_odd_numbers(self):
        """WindowSize handles very large odd numbers."""
        class Model(BaseModel):
            window_size: WindowSize

        for value in [10001, 100001, 999999]:
            model = Model(window_size=value)
            assert model.window_size == value

    def test_large_numbers_polynomial_order(self):
        """PolynomialOrder handles large numbers."""
        class Model(BaseModel):
            order: PolynomialOrder

        for value in [10000, 100000, 1000000]:
            model = Model(order=value)
            assert model.order == value

    def test_window_size_alternating_validation(self):
        """WindowSize alternates correctly between odd/even."""
        class Model(BaseModel):
            size: WindowSize

        for i in range(1, 20, 2):  # 1, 3, 5, 7, ...
            model = Model(size=i)
            assert model.size == i
            assert model.size % 2 == 1  # Verify it's odd

    def test_polynomial_order_all_positive_integers(self):
        """PolynomialOrder accepts all positive integers."""
        class Model(BaseModel):
            order: PolynomialOrder

        for i in range(1, 21):
            model = Model(order=i)
            assert model.order == i
            assert model.order > 0
