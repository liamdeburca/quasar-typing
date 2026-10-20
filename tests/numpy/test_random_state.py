"""Test RandomState types validation using pydantic TypeAdapter."""

import numpy as np
import pytest
from numpy.random import RandomState
from pydantic import TypeAdapter, ValidationError
from pydantic_core import PydanticCustomError

from quasar_typing.numpy.random import RandomStateType, StrictRandomStateType

# ============================================================================
# RandomStateType Tests (With Coercion)
# ============================================================================

def test_random_state_valid_seed_42(random_state_seed_42):
    """RandomState with seed 42 should pass validation."""
    adapter = TypeAdapter(RandomStateType)
    result = adapter.validate_python(random_state_seed_42)
    assert isinstance(result, RandomState)


def test_random_state_valid_seed_0(random_state_seed_0):
    """RandomState with seed 0 should pass validation."""
    adapter = TypeAdapter(RandomStateType)
    result = adapter.validate_python(random_state_seed_0)
    assert isinstance(result, RandomState)


def test_random_state_valid_seed_none(random_state_seed_none):
    """RandomState with None seed should pass validation."""
    adapter = TypeAdapter(RandomStateType)
    result = adapter.validate_python(random_state_seed_none)
    assert isinstance(result, RandomState)


def test_random_state_valid_seed_array(random_state_seed_array):
    """RandomState with array seed should pass validation."""
    adapter = TypeAdapter(RandomStateType)
    result = adapter.validate_python(random_state_seed_array)
    assert isinstance(result, RandomState)


def test_random_state_valid_default(random_state_default):
    """Default RandomState should pass validation."""
    adapter = TypeAdapter(RandomStateType)
    result = adapter.validate_python(random_state_default)
    assert isinstance(result, RandomState)


def test_random_state_valid_maintains_state(random_state_seed_42):
    """Validated RandomState should maintain its state."""
    _ = random_state_seed_42.rand()  # generate some random numbers
    original_state = random_state_seed_42.get_state()
    
    adapter = TypeAdapter(RandomStateType)
    result = adapter.validate_python(random_state_seed_42)
    # Should return the same object
    assert result is random_state_seed_42
    assert result.get_state()[1][0] == original_state[1][0]


def test_random_state_valid_large_seed():
    """RandomState with large seed should pass."""
    rng = RandomState(2**31 - 1)
    adapter = TypeAdapter(RandomStateType)
    result = adapter.validate_python(rng)
    assert isinstance(result, RandomState)


def test_random_state_rejects_float():
    """Float should not be accepted."""
    adapter = TypeAdapter(RandomStateType)
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python(42.0)


def test_random_state_rejects_string():
    """String should not be accepted."""
    adapter = TypeAdapter(RandomStateType)
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python("RandomState")


def test_random_state_rejects_dict():
    """Dictionary should not be accepted."""
    adapter = TypeAdapter(RandomStateType)
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python({"seed": 42})


def test_random_state_rejects_numpy_generator():
    """NumPy's new Generator should not be accepted."""
    rng = np.random.default_rng(42)
    adapter = TypeAdapter(RandomStateType)
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python(rng)


def test_random_state_rejects_custom_object():
    """Custom object should not be accepted."""
    class FakeRandomState:
        pass
    
    adapter = TypeAdapter(RandomStateType)
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python(FakeRandomState())


def test_random_state_multiple_instances_independent():
    """Multiple RandomState instances should validate independently."""
    rng1 = RandomState(42)
    rng2 = RandomState(43)
    
    adapter = TypeAdapter(RandomStateType)
    result1 = adapter.validate_python(rng1)
    result2 = adapter.validate_python(rng2)
    
    assert isinstance(result1, RandomState)
    assert isinstance(result2, RandomState)
    # They should be different objects
    assert result1 is not result2


def test_random_state_can_generate_random_numbers(random_state_seed_42):
    """Validated RandomState should still generate random numbers."""
    adapter = TypeAdapter(RandomStateType)
    result = adapter.validate_python(random_state_seed_42)
    value = result.rand()
    assert isinstance(value, (np.floating, float))
    assert 0.0 <= value <= 1.0


def test_random_state_reproducibility():
    """Same seed should produce same sequence."""
    rng1 = RandomState(42)
    rng2 = RandomState(42)
    
    adapter = TypeAdapter(RandomStateType)
    result1 = adapter.validate_python(rng1)
    result2 = adapter.validate_python(rng2)
    
    val1 = result1.rand()
    val2 = result2.rand()
    
    assert val1 == val2


# ============================================================================
# StrictRandomStateType Tests (No Coercion)
# ============================================================================

def test_strict_random_state_valid_seed_42(random_state_seed_42):
    """StrictRandomStateType with RandomState should pass."""
    adapter = TypeAdapter(StrictRandomStateType)
    result = adapter.validate_python(random_state_seed_42)
    assert isinstance(result, RandomState)


def test_strict_random_state_valid_default(random_state_default):
    """StrictRandomStateType with default RandomState should pass."""
    adapter = TypeAdapter(StrictRandomStateType)
    result = adapter.validate_python(random_state_default)
    assert isinstance(result, RandomState)


def test_strict_random_state_rejects_integer():
    """StrictRandomStateType should reject integer (no coercion)."""
    adapter = TypeAdapter(StrictRandomStateType)
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python(42)


def test_strict_random_state_rejects_float():
    """StrictRandomStateType should reject float."""
    adapter = TypeAdapter(StrictRandomStateType)
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python(42.0)


def test_strict_random_state_rejects_none():
    """StrictRandomStateType should reject None."""
    adapter = TypeAdapter(StrictRandomStateType)
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python(None)


def test_strict_random_state_rejects_list():
    """StrictRandomStateType should reject list."""
    adapter = TypeAdapter(StrictRandomStateType)
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python([1, 2, 3])


def test_strict_random_state_rejects_array():
    """StrictRandomStateType should reject array."""
    adapter = TypeAdapter(StrictRandomStateType)
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python(np.array([1, 2, 3]))


def test_strict_random_state_rejects_string():
    """StrictRandomStateType should reject string."""
    adapter = TypeAdapter(StrictRandomStateType)
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python("RandomState")


def test_strict_random_state_rejects_dict():
    """StrictRandomStateType should reject dict."""
    adapter = TypeAdapter(StrictRandomStateType)
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python({"seed": 42})


def test_strict_random_state_rejects_generator():
    """StrictRandomStateType should reject numpy Generator."""
    rng = np.random.default_rng(42)
    adapter = TypeAdapter(StrictRandomStateType)
    with pytest.raises((ValidationError, PydanticCustomError)):
        adapter.validate_python(rng)


# ============================================================================
# Reproducibility Tests
# ============================================================================

def test_random_state_deterministic_sequence():
    """Same seed should produce deterministic sequence."""
    rng1 = RandomState(12345)
    rng2 = RandomState(12345)
    
    adapter = TypeAdapter(RandomStateType)
    result1 = adapter.validate_python(rng1)
    result2 = adapter.validate_python(rng2)
    
    seq1 = result1.rand(10)
    seq2 = result2.rand(10)
    
    np.testing.assert_array_equal(seq1, seq2)


def test_random_state_different_seeds_different_sequences():
    """Different seeds should produce different sequences."""
    rng1 = RandomState(42)
    rng2 = RandomState(43)
    
    adapter = TypeAdapter(RandomStateType)
    result1 = adapter.validate_python(rng1)
    result2 = adapter.validate_python(rng2)
    
    seq1 = result1.rand(10)
    seq2 = result2.rand(10)
    
    # Very unlikely to be equal by chance
    assert not np.allclose(seq1, seq2)


def test_random_state_array_seed():
    """RandomState with array seed should work correctly."""
    seed_array = np.array([1, 2, 3, 4, 5])
    rng = RandomState(seed_array)
    
    adapter = TypeAdapter(RandomStateType)
    result = adapter.validate_python(rng)
    assert isinstance(result, RandomState)
    
    # Should be able to generate values
    value = result.rand()
    assert 0.0 <= value <= 1.0


# ============================================================================
# State Management Tests
# ============================================================================

def test_random_state_preserves_state():
    """Validation should not alter RandomState state."""
    rng = RandomState(42)
    
    # Generate some values
    val1 = rng.rand()
    state_before = rng.get_state()
    
    # Validate
    adapter = TypeAdapter(RandomStateType)
    result = adapter.validate_python(rng)
    state_after = result.get_state()
    
    # Generate next value
    val2 = result.rand()
    
    # Validate doesn't change state
    assert state_before[0] == state_after[0]


def test_random_state_returns_same_object():
    """Validation should return the same object, not a copy."""
    rng = RandomState(42)
    adapter = TypeAdapter(RandomStateType)
    result = adapter.validate_python(rng)
    assert result is rng


def test_random_state_int_choice():
    """RandomState should be able to make integer choices."""
    rng = RandomState(42)
    adapter = TypeAdapter(RandomStateType)
    result = adapter.validate_python(rng)
    
    choice = result.choice(10)
    assert isinstance(choice, (np.integer, int))
    assert 0 <= choice < 10


def test_random_state_normal_distribution():
    """RandomState should generate from normal distribution."""
    rng = RandomState(42)
    adapter = TypeAdapter(RandomStateType)
    result = adapter.validate_python(rng)
    
    values = result.randn(100)
    assert isinstance(values, np.ndarray)
    assert values.size == 100
    # Should have roughly normal distribution
    assert abs(values.mean()) < 1.0  # Loose check for mean near 0


def test_random_state_uniform_distribution():
    """RandomState should generate uniform distribution."""
    rng = RandomState(42)
    adapter = TypeAdapter(RandomStateType)
    result = adapter.validate_python(rng)
    
    values = result.uniform(0, 1, size=100)
    assert isinstance(values, np.ndarray)
    assert values.size == 100
    assert values.min() >= 0
    assert values.max() <= 1
