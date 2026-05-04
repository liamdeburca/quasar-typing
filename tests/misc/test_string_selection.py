import pytest
from pydantic import validate_call
from pydantic_core import ValidationError
from quasar_typing.misc import StringSelection


class BackgroundFlux(StringSelection):
    """Test subclass with defined string options."""
    _string_options = ('all', 'pl', 'fe', 'ba', 'hg', 'em')


class TestStringSelectionWithoutAll:
    """Test StringSelection behavior when 'all' is NOT in the selection."""
    
    def test_single_option(self):
        """Test selecting a single option."""
        selection = BackgroundFlux({'pl'})
        assert selection == {'pl'}
        assert 'pl' in selection
        assert 'fe' not in selection
    
    def test_multiple_options(self):
        """Test selecting multiple options."""
        selection = BackgroundFlux({'pl', 'fe', 'ba'})
        assert selection == {'pl', 'fe', 'ba'}
        assert 'pl' in selection
        assert 'fe' in selection
        assert 'ba' in selection
        assert 'hg' not in selection
        assert 'em' not in selection
    
    def test_explicit_options_exclude_others(self):
        """Test that explicitly selected options exclude all others."""
        selection = BackgroundFlux({'pl'})
        assert selection == {'pl'}
        assert len(selection) == 1


class TestStringSelectionWithAll:
    """Test StringSelection behavior when 'all' IS in the selection."""
    
    def test_all_alone_includes_everything(self):
        """Test that 'all' alone includes all options."""
        selection = BackgroundFlux({'all'})
        assert selection == {'pl', 'fe', 'ba', 'hg', 'em'}
    
    def test_all_with_single_exclusion(self):
        """Test 'all' with one option excluded."""
        selection = BackgroundFlux({'all', 'pl'})
        assert selection == {'fe', 'ba', 'hg', 'em'}
    
    def test_all_with_multiple_exclusions(self):
        """Test 'all' with multiple options excluded."""
        selection = BackgroundFlux({'all', 'pl', 'fe'})
        assert selection == {'ba', 'hg', 'em'}
    
    def test_all_with_many_exclusions(self):
        """Test 'all' with most options excluded."""
        selection = BackgroundFlux({'all', 'pl', 'fe', 'ba', 'hg'})
        assert selection == {'em'}
    
    def test_all_with_all_options_excluded(self):
        """Test 'all' with all actual options excluded."""
        selection = BackgroundFlux({'all', 'pl', 'fe', 'ba', 'hg', 'em'})
        assert selection == set()


class TestStringSelectionValidation:
    """Test validation and error handling."""
    
    def test_list_input(self):
        """Test that lists are accepted."""
        selection = BackgroundFlux(['pl', 'fe'])
        assert selection == {'pl', 'fe'}
    
    def test_tuple_input(self):
        """Test that tuples are accepted."""
        selection = BackgroundFlux(('pl', 'fe'))
        assert selection == {'pl', 'fe'}
    
    def test_frozenset_input(self):
        """Test that frozensets are accepted."""
        selection = BackgroundFlux(frozenset({'pl', 'fe'}))
        assert selection == {'pl', 'fe'}
    
    def test_duplicate_options(self):
        """Test that duplicate options are handled correctly."""
        selection = BackgroundFlux({'pl', 'pl', 'fe', 'fe'})
        assert selection == {'pl', 'fe'}
    
    def test_invalid_type_raises_error(self):
        """Test that invalid types raise an error through pydantic validation."""
        @validate_call
        def validate_background_flux(value: BackgroundFlux) -> BackgroundFlux:
            return value
        
        with pytest.raises(ValidationError):
            validate_background_flux("not a set")
            pass
    
    def test_non_string_items_raise_error(self):
        """Test that non-string items raise an error through pydantic validation."""
        @validate_call
        def validate_background_flux(value: BackgroundFlux) -> BackgroundFlux:
            return value
        
        with pytest.raises(ValidationError):
            validate_background_flux(['pl', 123, 'fe'])
            pass

class TestStringSelectionEdgeCases:
    """Test edge cases and special behavior."""
    
    def test_set_operations(self):
        """Test that set operations work correctly."""
        sel1 = BackgroundFlux({'pl', 'fe'})
        sel2 = BackgroundFlux({'fe', 'ba'})
        
        # Intersection
        assert sel1 & sel2 == {'fe'}
        # Union
        assert sel1 | sel2 == {'pl', 'fe', 'ba'}
        # Difference
        assert sel1 - sel2 == {'pl'}
    
    def test_membership(self):
        """Test membership testing."""
        selection = BackgroundFlux({'pl', 'fe'})
        assert 'pl' in selection
        assert 'fe' in selection
        assert 'ba' not in selection
    
    def test_length(self):
        """Test length of selection."""
        selection = BackgroundFlux({'pl', 'fe', 'ba'})
        assert len(selection) == 3
    
    def test_iteration(self):
        """Test iteration over selection."""
        selection = BackgroundFlux({'pl', 'fe'})
        items = list(selection)
        assert set(items) == {'pl', 'fe'}
        assert len(items) == 2



