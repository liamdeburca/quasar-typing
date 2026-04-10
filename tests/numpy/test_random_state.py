"""Unit tests for RandomState_ type validation."""

import pytest
import numpy as np
from numpy.random import RandomState

from quasar_typing.numpy import RandomState_


class TestRandomState:
    """Test RandomState_ validation."""
    
    def test_valid_random_state_with_seed(self):
        """Valid RandomState with seed should pass validation."""
        rng = RandomState(42)
        result = RandomState_._validate(rng)
        assert isinstance(result, RandomState)
    
    def test_valid_random_state_with_large_seed(self):
        """RandomState with large seed should pass."""
        rng = RandomState(2**31 - 1)
        result = RandomState_._validate(rng)
        assert isinstance(result, RandomState)
    
    def test_valid_random_state_with_zero_seed(self):
        """RandomState with zero seed should pass."""
        rng = RandomState(0)
        result = RandomState_._validate(rng)
        assert isinstance(result, RandomState)
    
    def test_valid_random_state_with_none_seed(self):
        """RandomState with None seed should pass (uses system time)."""
        rng = RandomState(None)
        result = RandomState_._validate(rng)
        assert isinstance(result, RandomState)
    
    def test_valid_random_state_with_array_seed(self):
        """RandomState with array seed should pass."""
        seed_array = np.array([1, 2, 3, 4, 5])
        rng = RandomState(seed_array)
        result = RandomState_._validate(rng)
        assert isinstance(result, RandomState)
    
    def test_valid_random_state_default(self):
        """Default RandomState should pass."""
        rng = RandomState()
        result = RandomState_._validate(rng)
        assert isinstance(result, RandomState)
    
    def test_valid_random_state_maintains_state(self):
        """Validated RandomState should maintain its state."""
        rng = RandomState(42)
        _ = rng.rand()  # generate some random numbers
        original_state = rng.get_state()
        
        result = RandomState_._validate(rng)
        # Should return the same object
        assert result is rng
        assert result.get_state()[1][0] == original_state[1][0]
    
    def test_invalid_integer_input(self):
        """Integer input should raise error."""
        with pytest.raises(Exception) as exc_info:
            RandomState_._validate(42)
        assert 'Expected numpy RandomState' in str(exc_info.value)
    
    def test_invalid_float_input(self):
        """Float input should raise error."""
        with pytest.raises(Exception) as exc_info:
            RandomState_._validate(42.0)
        assert 'Expected numpy RandomState' in str(exc_info.value)
    
    def test_invalid_none_input(self):
        """None input should raise error."""
        with pytest.raises(Exception) as exc_info:
            RandomState_._validate(None)
        assert 'Expected numpy RandomState' in str(exc_info.value)
    
    def test_invalid_list_input(self):
        """List input should raise error."""
        with pytest.raises(Exception) as exc_info:
            RandomState_._validate([1, 2, 3])
        assert 'Expected numpy RandomState' in str(exc_info.value)
    
    def test_invalid_array_input(self):
        """NumPy array input should raise error."""
        with pytest.raises(Exception) as exc_info:
            RandomState_._validate(np.array([1, 2, 3]))
        assert 'Expected numpy RandomState' in str(exc_info.value)
    
    def test_invalid_string_input(self):
        """String input should raise error."""
        with pytest.raises(Exception) as exc_info:
            RandomState_._validate("RandomState")
        assert 'Expected numpy RandomState' in str(exc_info.value)
    
    def test_invalid_dict_input(self):
        """Dictionary input should raise error."""
        with pytest.raises(Exception) as exc_info:
            RandomState_._validate({"seed": 42})
        assert 'Expected numpy RandomState' in str(exc_info.value)
    
    def test_invalid_tuple_input(self):
        """Tuple input should raise error."""
        with pytest.raises(Exception) as exc_info:
            RandomState_._validate((42,))
        assert 'Expected numpy RandomState' in str(exc_info.value)
    
    def test_invalid_numpy_generator(self):
        """NumPy's new Generator should not pass RandomState_ validation."""
        rng = np.random.default_rng(42)
        with pytest.raises(Exception) as exc_info:
            RandomState_._validate(rng)
        assert 'Expected numpy RandomState' in str(exc_info.value)
    
    def test_invalid_custom_object(self):
        """Custom object should raise error."""
        class FakeRandomState:
            pass
        
        with pytest.raises(Exception) as exc_info:
            RandomState_._validate(FakeRandomState())
        assert 'Expected numpy RandomState' in str(exc_info.value)
    
    def test_error_message_includes_type(self):
        """Error message should include the actual type."""
        with pytest.raises(Exception) as exc_info:
            RandomState_._validate("not a RandomState")
        error_msg = str(exc_info.value)
        assert 'Expected numpy RandomState' in error_msg
        assert "<class 'str'>" in error_msg or "str" in error_msg
    
    def test_valid_multiple_random_states_independent(self):
        """Multiple RandomState instances should validate independently."""
        rng1 = RandomState(42)
        rng2 = RandomState(43)
        
        result1 = RandomState_._validate(rng1)
        result2 = RandomState_._validate(rng2)
        
        assert isinstance(result1, RandomState)
        assert isinstance(result2, RandomState)
        # They should be different objects
        assert result1 is not result2
    
    def test_valid_random_state_can_generate_random_numbers(self):
        """Validated RandomState should still be able to generate random numbers."""
        rng = RandomState(42)
        result = RandomState_._validate(rng)
        
        # Should be able to call random methods
        rand_num = result.rand()
        assert isinstance(rand_num, (float, np.floating))
        assert 0 <= rand_num <= 1
    
    def test_valid_random_state_seed_parameter_types(self):
        """RandomState should accept various seed types."""
        seed_values = [
            42,
            0,
            2**31 - 1,
            None,
            np.uint32(42),
        ]
        
        for seed in seed_values:
            rng = RandomState(seed)
            result = RandomState_._validate(rng)
            assert isinstance(result, RandomState)
