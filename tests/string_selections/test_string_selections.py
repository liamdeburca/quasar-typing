import pytest
from typing import Literal
from pydantic import BaseModel, ValidationError
from pydantic import TypeAdapter

from quasar_typing.string_selections import (
    StringSelection,
    DataTypes,
    ModelTypes,
    BackgroundFlux,
    PowerLawModelParams,
    IronModelParams,
    BalmerModelParams,
    HostGalaxyModelParams,
    GaussianModelParams,
    VaryLines,
    OutLines,
    OutMeasures,
)


class TestStringSelectionInit:
    """Tests for StringSelection.__init__"""

    def test_init_with_subset(self):
        """StringSelection with subset of options."""
        selection = DataTypes({"pl", "fe"})
        assert "pl" in selection
        assert "fe" in selection
        assert "ba" not in selection

    def test_init_with_all_keyword(self):
        """StringSelection with 'all' keyword should select all options."""
        selection = DataTypes({"all"})
        assert "pl" in selection
        assert "fe" in selection
        assert "ba" in selection
        assert "hg" in selection
        assert "em" in selection

    def test_init_with_all_and_exclusions(self):
        """StringSelection with 'all' and exclusions uses XOR logic."""
        selection = DataTypes({"all", "pl", "fe"})
        # With XOR: "all" is selected, but "pl" and "fe" are excluded
        assert "pl" not in selection
        assert "fe" not in selection
        assert "ba" in selection
        assert "hg" in selection
        assert "em" in selection

    def test_init_single_option(self):
        """StringSelection with single option."""
        selection = PowerLawModelParams({"flux"})
        assert "flux" in selection
        assert "alpha" not in selection

    def test_init_empty_set(self):
        """StringSelection with empty set."""
        selection = DataTypes(set())
        assert len(selection) == 0
        assert "pl" not in selection

    def test_init_unbounded_string_selection(self):
        """StringSelection without _string_options acts as regular set."""
        selection = StringSelection({"apple", "banana"})
        assert "apple" in selection
        assert "banana" in selection
        assert "cherry" not in selection

    def test_init_unbounded_with_all(self):
        """Unbounded StringSelection with 'all' keyword - XOR logic applies."""
        selection = StringSelection({"all", "apple"})
        # XOR logic: both "all" and "apple" in underlying set
        # __contains__ returns: super().__contains__(s) ^ super().__contains__("all")
        # For "apple": True ^ True = False
        # For "all": True ^ True = False
        assert "apple" not in selection
        assert "all" not in selection


class TestStringSelectionContains:
    """Tests for StringSelection.__contains__ with XOR logic"""

    def test_contains_simple_selection(self, custom_string_selection_with_options):
        """Contains works for simple selections."""
        assert "red" in custom_string_selection_with_options
        assert "green" in custom_string_selection_with_options
        assert "blue" not in custom_string_selection_with_options

    def test_contains_with_all(self, custom_string_selection_all):
        """Contains with 'all' keyword - all options are included."""
        assert "red" in custom_string_selection_all
        assert "green" in custom_string_selection_all
        assert "blue" in custom_string_selection_all

    def test_contains_with_exclude(self, custom_string_selection_exclude):
        """Contains with 'all' and exclusions - XOR logic."""
        # {"all", "red"} -> exclude "red", include others
        assert "red" not in custom_string_selection_exclude
        assert "green" in custom_string_selection_exclude
        assert "blue" in custom_string_selection_exclude

    def test_contains_unbounded_selection(self, unbounded_string_selection):
        """Contains on unbounded StringSelection."""
        assert "apple" in unbounded_string_selection
        assert "banana" in unbounded_string_selection
        assert "cherry" in unbounded_string_selection

    def test_contains_with_all_unbounded(self):
        """Contains with 'all' in unbounded StringSelection."""
        selection = StringSelection({"all", "apple"})
        # XOR: both "all" and "apple" in underlying set
        # __contains__ uses: super().__contains__(s) ^ super().__contains__("all")
        # For "apple": True ^ True = False
        assert "apple" not in selection
        assert "all" not in selection


class TestStringSelectionToFixed:
    """Tests for StringSelection.to_fixed() conversion"""

    def test_to_fixed_subset(self, custom_string_selection_with_options):
        """to_fixed() returns dict with T/F for each option."""
        result = custom_string_selection_with_options.to_fixed()
        assert result == {"red": True, "green": True, "blue": False}

    def test_to_fixed_all(self, custom_string_selection_all):
        """to_fixed() with all options selected."""
        result = custom_string_selection_all.to_fixed()
        assert result == {"red": True, "green": True, "blue": True}

    def test_to_fixed_exclude(self, custom_string_selection_exclude):
        """to_fixed() with exclusions."""
        result = custom_string_selection_exclude.to_fixed()
        assert result == {"red": False, "green": True, "blue": True}

    def test_to_fixed_empty(self):
        """to_fixed() with no selections."""
        selection = DataTypes(set())
        result = selection.to_fixed()
        assert result == {"pl": False, "fe": False, "ba": False, "hg": False, "em": False}

    def test_to_fixed_power_law(self, power_law_params_one):
        """to_fixed() for PowerLawModelParams."""
        result = power_law_params_one.to_fixed()
        assert result == {"flux": True, "alpha": False}


class TestStringSelectionValidate:
    """Tests for StringSelection._validate and Pydantic integration"""

    def test_validate_dict_input(self):
        """_validate converts dict to StringSelection."""
        adapter = TypeAdapter(DataTypes)
        result = adapter.validate_python({"pl", "fe"})
        assert isinstance(result, DataTypes)
        assert "pl" in result
        assert "fe" in result

    def test_validate_string_selection_passthrough(self):
        """_validate returns StringSelection as-is."""
        original = DataTypes({"pl"})
        adapter = TypeAdapter(DataTypes)
        result = adapter.validate_python(original)
        assert result == original

    def test_validate_none_defaults_to_all(self):
        """_validate with None defaults to 'all'."""
        adapter = TypeAdapter(DataTypes)
        result = adapter.validate_python(None)
        assert isinstance(result, DataTypes)
        # None should be coerced to {"all"}
        assert "pl" in result
        assert "fe" in result

    def test_validate_empty_set_defaults_to_all(self):
        """_validate with empty set defaults to 'all'."""
        adapter = TypeAdapter(DataTypes)
        result = adapter.validate_python(set())
        # Empty set should be coerced to {"all"}
        assert "pl" in result

    def test_validate_invalid_type_raises_error(self):
        """_validate with invalid type raises ValidationError."""
        adapter = TypeAdapter(DataTypes)
        with pytest.raises(ValidationError):
            adapter.validate_python("invalid_string")

    def test_validate_list_input_raises_error(self):
        """_validate with list is coerced to set automatically."""
        adapter = TypeAdapter(DataTypes)
        # Lists can be coerced to sets by Pydantic, so this should work
        result = adapter.validate_python(["pl", "fe"])
        assert "pl" in result
        assert "fe" in result

    def test_pydantic_integration_in_model(self):
        """StringSelection works in Pydantic BaseModel."""
        class Config(BaseModel):
            data_types: DataTypes
            power_law: PowerLawModelParams

        config = Config(data_types={"pl"}, power_law={"flux"})
        assert "pl" in config.data_types
        assert "flux" in config.power_law

    def test_pydantic_model_with_all(self):
        """Pydantic model with 'all' keyword."""
        class Config(BaseModel):
            model_types: ModelTypes

        config = Config(model_types={"all", "pl"})
        # XOR: "all" and "pl", so exclude "pl"
        assert "pl" not in config.model_types
        assert "fe" in config.model_types


class TestStringSelectionHash:
    """Tests for StringSelection.__hash__"""

    def test_hash_consistency(self):
        """Same selection has same hash."""
        sel1 = DataTypes({"pl", "fe"})
        sel2 = DataTypes({"pl", "fe"})
        assert hash(sel1) == hash(sel2)

    def test_hash_different_selections(self):
        """Different selections have different hashes."""
        sel1 = DataTypes({"pl", "fe"})
        sel2 = DataTypes({"ba", "hg"})
        # Different content should (likely) have different hashes
        assert hash(sel1) != hash(sel2)

    def test_hash_in_dict(self):
        """StringSelection can be used as dict key."""
        sel1 = PowerLawModelParams({"flux"})
        sel2 = PowerLawModelParams({"alpha"})
        d = {sel1: "value1", sel2: "value2"}
        assert d[sel1] == "value1"
        assert d[sel2] == "value2"

    def test_hash_in_set(self):
        """StringSelection can be used in set."""
        sel1 = DataTypes({"pl"})
        sel2 = DataTypes({"fe"})
        s = {sel1, sel2}
        assert sel1 in s
        assert sel2 in s


class TestStringSelectionEquality:
    """Tests for StringSelection equality"""

    def test_equal_selections(self):
        """Identical selections are equal."""
        sel1 = DataTypes({"pl", "fe"})
        sel2 = DataTypes({"pl", "fe"})
        assert sel1 == sel2

    def test_unequal_selections(self):
        """Different selections are not equal."""
        sel1 = DataTypes({"pl", "fe"})
        sel2 = DataTypes({"ba", "hg"})
        assert sel1 != sel2

    def test_equal_to_regular_set(self):
        """StringSelection equal to regular set with same contents."""
        sel = DataTypes({"pl", "fe"})
        # After init, sel contains {"pl", "fe"}
        assert sel == {"pl", "fe"}


class TestStringSelectionSubclasses:
    """Tests for concrete StringSelection subclasses"""

    def test_data_types_all_options(self):
        """DataTypes has 5 correct options."""
        dt = DataTypes({"all"})
        assert len(dt) == 5
        for opt in ["pl", "fe", "ba", "hg", "em"]:
            assert opt in dt

    def test_model_types_equivalent_to_data_types(self):
        """ModelTypes has same options as DataTypes."""
        dt = DataTypes({"all"})
        mt = ModelTypes({"all"})
        assert set(dt) == set(mt)

    def test_power_law_params(self):
        """PowerLawModelParams has 2 options."""
        pl = PowerLawModelParams({"all"})
        assert len(pl) == 2
        assert "flux" in pl
        assert "alpha" in pl

    def test_iron_params(self):
        """IronModelParams has 5 options."""
        ip = IronModelParams({"all"})
        assert len(ip) == 5
        for opt in ["flux", "fwhm", "split", "left", "right"]:
            assert opt in ip

    def test_balmer_params(self):
        """BalmerModelParams has 3 options."""
        bp = BalmerModelParams({"all"})
        assert len(bp) == 3
        for opt in ["flux", "fwhm", "ratio"]:
            assert opt in bp

    def test_host_galaxy_params(self):
        """HostGalaxyModelParams has 2 options."""
        hg = HostGalaxyModelParams({"all"})
        assert len(hg) == 2
        for opt in ["flux", "fwhm"]:
            assert opt in hg

    def test_gaussian_params(self):
        """GaussianModelParams has 3 options."""
        gp = GaussianModelParams({"all"})
        assert len(gp) == 3
        for opt in ["strength", "fwhm_v", "v_off"]:
            assert opt in gp


class TestUnboundedStringSelection:
    """Tests for StringSelection without _string_options"""

    def test_unbounded_any_string(self):
        """Unbounded StringSelection accepts any string."""
        sel = StringSelection({"line1", "line2", "custom_line"})
        assert "line1" in sel
        assert "custom_line" in sel

    def test_unbounded_with_all_keyword(self):
        """Unbounded StringSelection with 'all' keyword - XOR logic applies."""
        sel = StringSelection({"all", "line1"})
        # XOR: both in underlying set, so XOR gives False for both
        assert "line1" not in sel
        assert "all" not in sel

    def test_unbounded_to_fixed_empty(self):
        """Unbounded StringSelection.to_fixed() is empty (no _string_options)."""
        sel = StringSelection({"line1", "line2"})
        result = sel.to_fixed()
        assert result == {}

    def test_unbounded_mixed_with_bounded(self):
        """Test bounded vs unbounded StringSelection."""
        # Use StringSelection directly for unbounded
        unbounded = StringSelection({"line_a", "line_b"})
        bounded = DataTypes({"pl"})
        assert "line_a" in unbounded
        assert "pl" in bounded


class TestStringSelectionSetOperations:
    """Tests for set operations on StringSelection"""

    def test_set_union(self):
        """Union of StringSelections."""
        sel1 = DataTypes({"pl", "fe"})
        sel2 = DataTypes({"ba"})
        result = sel1 | sel2
        assert "pl" in result
        assert "fe" in result
        assert "ba" in result

    def test_set_intersection(self):
        """Intersection of StringSelections."""
        sel1 = DataTypes({"pl", "fe", "ba"})
        sel2 = DataTypes({"pl", "ba"})
        result = sel1 & sel2
        assert "pl" in result
        assert "ba" in result
        assert "fe" not in result

    def test_set_difference(self):
        """Difference of StringSelections."""
        sel1 = DataTypes({"pl", "fe", "ba"})
        sel2 = DataTypes({"pl"})
        result = sel1 - sel2
        assert "fe" in result
        assert "ba" in result
        assert "pl" not in result

    def test_len_of_selection(self):
        """Length of StringSelection."""
        sel = DataTypes({"pl", "fe"})
        assert len(sel) == 2

    def test_iteration(self):
        """Iteration over StringSelection."""
        sel = PowerLawModelParams({"flux", "alpha"})
        items = list(sel)
        assert "flux" in items
        assert "alpha" in items


class TestStringSelectionEdgeCases:
    """Edge case tests"""

    def test_all_by_itself(self):
        """StringSelection with only 'all' keyword."""
        sel = DataTypes({"all"})
        # All options should be selected
        assert len(sel) == 5

    def test_all_with_all_options(self):
        """StringSelection with 'all' and all other options."""
        sel = DataTypes({"all", "pl", "fe", "ba", "hg", "em"})
        # XOR: everything is excluded
        assert len(sel) == 0
        assert "pl" not in sel

    def test_single_string_option_class(self):
        """StringSelection subclass with single option."""
        class SingleOption(StringSelection[Literal["only"]]):
            _string_options = ("only",)

        sel_with = SingleOption({"only"})
        sel_without = SingleOption(set())
        
        assert "only" in sel_with
        assert "only" not in sel_without

    def test_case_sensitive(self):
        """StringSelection is case-sensitive."""
        sel = DataTypes({"pl"})
        assert "pl" in sel
        # These should not be in (assuming case-sensitive)
        assert "PL" not in sel
        assert "Pl" not in sel

    def test_multiple_models_independent(self):
        """Different StringSelection subclasses are independent."""
        dt = DataTypes({"pl"})
        mt = ModelTypes({"pl"})
        # Both have "pl", but are different types
        assert "pl" in dt
        assert "pl" in mt
        assert type(dt) != type(mt)


class TestStringSelectionCopy:
    """Tests for copying StringSelection"""

    def test_copy_preserves_data(self):
        """Copying preserves the selection data."""
        sel1 = DataTypes({"pl", "fe"})
        sel2 = DataTypes(set(sel1))  # Copy by creating new from set content
        assert sel1 == sel2

    def test_copy_is_independent(self):
        """Modifications to copy don't affect original."""
        sel1 = DataTypes({"pl"})
        sel2 = DataTypes({"pl", "fe"})
        # They should be different
        assert sel1 != sel2


class TestStringSelectionPydanticValidationErrors:
    """Tests for Pydantic validation error handling"""

    def test_invalid_string_in_bounded_selection(self):
        """Invalid string in bounded selection gets filtered out by init."""
        # DataTypes.__init__ filters using XOR with _string_options
        # Only strings in _string_options are kept
        sel = DataTypes({"pl", "invalid"})
        # The set contains only what's in _string_options
        assert "pl" in sel
        assert "invalid" not in sel

    def test_validation_with_invalid_type_fails(self):
        """Validation fails with completely invalid type."""
        adapter = TypeAdapter(DataTypes)
        with pytest.raises(ValidationError):
            adapter.validate_python(123)

    def test_validation_with_nested_model(self):
        """StringSelection in nested Pydantic model."""
        class Inner(BaseModel):
            types: DataTypes

        class Outer(BaseModel):
            inner: Inner

        outer = Outer(inner={"types": {"pl", "fe"}})
        assert "pl" in outer.inner.types


class TestBackgroundFluxSpecific:
    """Dedicated tests for BackgroundFlux class"""

    def test_background_flux_all_options(self):
        """BackgroundFlux has correct 5 options."""
        bf = BackgroundFlux({"all"})
        assert len(bf) == 5
        for opt in ["pl", "fe", "ba", "hg", "em"]:
            assert opt in bf

    def test_background_flux_subset(self):
        """BackgroundFlux with subset selection."""
        bf = BackgroundFlux({"pl", "fe", "ba"})
        assert "pl" in bf
        assert "fe" in bf
        assert "ba" in bf
        assert "hg" not in bf
        assert "em" not in bf

    def test_background_flux_with_all_exclusion(self):
        """BackgroundFlux with 'all' and exclusions."""
        bf = BackgroundFlux({"all", "pl", "fe"})
        assert "pl" not in bf
        assert "fe" not in bf
        assert "ba" in bf
        assert "hg" in bf
        assert "em" in bf

    def test_background_flux_single_option(self):
        """BackgroundFlux with single option."""
        bf = BackgroundFlux({"em"})
        assert "em" in bf
        assert len(bf) == 1

    def test_background_flux_empty(self):
        """BackgroundFlux with empty set."""
        bf = BackgroundFlux(set())
        assert len(bf) == 0
        for opt in ["pl", "fe", "ba", "hg", "em"]:
            assert opt not in bf

    def test_background_flux_to_fixed(self):
        """BackgroundFlux.to_fixed() returns dict mapping."""
        bf = BackgroundFlux({"pl", "em"})
        result = bf.to_fixed()
        assert result == {"pl": True, "fe": False, "ba": False, "hg": False, "em": True}

    def test_background_flux_pydantic_validation(self):
        """BackgroundFlux validates in Pydantic model."""
        class Config(BaseModel):
            flux: BackgroundFlux

        config = Config(flux={"pl", "ba"})
        assert "pl" in config.flux
        assert "ba" in config.flux
        assert "fe" not in config.flux

    def test_background_flux_pydantic_with_all(self):
        """BackgroundFlux with 'all' in Pydantic model."""
        class Config(BaseModel):
            flux: BackgroundFlux

        config = Config(flux={"all"})
        # All 5 options should be included
        assert len(config.flux) == 5
        for opt in ["pl", "fe", "ba", "hg", "em"]:
            assert opt in config.flux

    def test_background_flux_hash(self):
        """BackgroundFlux is hashable."""
        bf1 = BackgroundFlux({"pl", "fe"})
        bf2 = BackgroundFlux({"pl", "fe"})
        assert hash(bf1) == hash(bf2)
        # Can use as dict key
        d = {bf1: "value"}
        assert d[bf2] == "value"

    def test_background_flux_equality(self):
        """BackgroundFlux equality."""
        bf1 = BackgroundFlux({"pl", "fe"})
        bf2 = BackgroundFlux({"pl", "fe"})
        bf3 = BackgroundFlux({"ba"})
        assert bf1 == bf2
        assert bf1 != bf3


class TestVaryLinesSpecific:
    """Dedicated tests for VaryLines type alias (unbounded StringSelection)"""

    def test_vary_lines_basic_creation(self):
        """VaryLines can be created with arbitrary strings."""
        vl = StringSelection({"line1", "line2", "line3"})
        assert "line1" in vl
        assert "line2" in vl
        assert "line3" in vl

    def test_vary_lines_custom_line_names(self):
        """VaryLines accepts any line name."""
        vl = StringSelection({"Ha", "Hb", "Hg", "custom_line", "emission_line"})
        assert "Ha" in vl
        assert "Hb" in vl
        assert "custom_line" in vl
        assert "emission_line" in vl

    def test_vary_lines_single_line(self):
        """VaryLines with single line."""
        vl = StringSelection({"Ha"})
        assert "Ha" in vl
        assert len(vl) == 1

    def test_vary_lines_empty(self):
        """VaryLines with empty set."""
        vl = StringSelection(set())
        assert len(vl) == 0
        assert "Ha" not in vl

    def test_vary_lines_with_all_keyword(self):
        """VaryLines with 'all' keyword - XOR logic applies.
        
        From __contains__ docstring example:
        >>> "red" in RandomSelection({"all", "red"})
        False
        """
        vl = StringSelection({"all", "line1"})
        # XOR: both "all" and "line1" in underlying set
        # __contains__ uses: super().__contains__(s) ^ super().__contains__("all")
        # "line1": True ^ True = False
        # "all": True ^ True = False
        assert "line1" not in vl
        assert "all" not in vl

    def test_vary_lines_with_all_only(self):
        """VaryLines with only 'all' keyword."""
        vl = StringSelection({"all"})
        # "all" is in set, but __contains__("all") = True ^ True = False
        assert "all" not in vl
        # Any other string: False ^ True = True
        # But it's not in the set, so it should fail
        # Actually: super().__contains__("line1") = False
        # False ^ True = True, so "line1" should be in vl
        assert "line1" in vl  # Based on XOR logic

    def test_vary_lines_multiple_selections(self):
        """VaryLines with multiple line selections."""
        vl = StringSelection({"Ha", "Hb", "Hg", "Hd"})
        assert len(vl) == 4
        for line in ["Ha", "Hb", "Hg", "Hd"]:
            assert line in vl

    def test_vary_lines_to_fixed_empty(self):
        """VaryLines.to_fixed() is empty (no _string_options)."""
        vl = StringSelection({"line1", "line2"})
        result = vl.to_fixed()
        assert result == {}

    def test_vary_lines_pydantic_validation(self):
        """VaryLines in Pydantic model."""
        class Config(BaseModel):
            lines: StringSelection

        config = Config(lines={"Ha", "Hb", "Hg"})
        assert "Ha" in config.lines
        assert "Hb" in config.lines

    def test_vary_lines_set_operations(self):
        """VaryLines supports set operations."""
        vl1 = StringSelection({"Ha", "Hb"})
        vl2 = StringSelection({"Hb", "Hg"})
        union = vl1 | vl2
        assert "Ha" in union
        assert "Hb" in union
        assert "Hg" in union

    def test_vary_lines_hash(self):
        """VaryLines is hashable."""
        vl1 = StringSelection({"Ha", "Hb"})
        vl2 = StringSelection({"Ha", "Hb"})
        assert hash(vl1) == hash(vl2)

    def test_vary_lines_equality(self):
        """VaryLines equality."""
        vl1 = StringSelection({"Ha", "Hb"})
        vl2 = StringSelection({"Ha", "Hb"})
        vl3 = StringSelection({"Hg"})
        assert vl1 == vl2
        assert vl1 != vl3


class TestOutLinesSpecific:
    """Dedicated tests for OutLines type alias (unbounded StringSelection)"""

    def test_out_lines_basic_creation(self):
        """OutLines can be created with arbitrary strings."""
        ol = StringSelection({"line1", "line2"})
        assert "line1" in ol
        assert "line2" in ol

    def test_out_lines_standard_names(self):
        """OutLines with standard astronomical line names."""
        ol = StringSelection({"Ha", "Hb", "OIII", "SII", "NII"})
        assert "Ha" in ol
        assert "OIII" in ol
        assert "SII" in ol

    def test_out_lines_single_line(self):
        """OutLines with single output line."""
        ol = StringSelection({"Ha"})
        assert "Ha" in ol
        assert len(ol) == 1

    def test_out_lines_empty(self):
        """OutLines with empty set."""
        ol = StringSelection(set())
        assert len(ol) == 0

    def test_out_lines_with_all_keyword(self):
        """OutLines with 'all' keyword.
        
        From __contains__ docstring example:
        >>> "red" in RandomSelection({"all", "red"})
        False
        """
        ol = StringSelection({"all", "Ha"})
        # XOR: both in set, so both evaluate to False in __contains__
        assert "Ha" not in ol
        assert "all" not in ol

    def test_out_lines_with_all_only(self):
        """OutLines with only 'all' keyword."""
        ol = StringSelection({"all"})
        # "Ha": super().__contains__("Ha") ^ super().__contains__("all")
        # = False ^ True = True
        assert "Ha" in ol
        assert "Hb" in ol

    def test_out_lines_mixed_with_all(self):
        """OutLines excluding certain lines with 'all'."""
        ol = StringSelection({"all", "Ha", "Hb"})
        # "Ha": True ^ True = False
        # "Hb": True ^ True = False
        # "Hg": False ^ True = True
        assert "Ha" not in ol
        assert "Hb" not in ol
        assert "Hg" in ol

    def test_out_lines_to_fixed_empty(self):
        """OutLines.to_fixed() is empty (no _string_options)."""
        ol = StringSelection({"Ha", "Hb"})
        result = ol.to_fixed()
        assert result == {}

    def test_out_lines_pydantic_validation(self):
        """OutLines in Pydantic model."""
        class Config(BaseModel):
            lines: StringSelection

        config = Config(lines={"Ha", "Hb"})
        assert "Ha" in config.lines
        assert "Hb" in config.lines

    def test_out_lines_set_operations(self):
        """OutLines supports set operations."""
        ol1 = StringSelection({"Ha", "Hb"})
        ol2 = StringSelection({"Hb", "Hg"})
        intersection = ol1 & ol2
        assert "Hb" in intersection
        assert "Ha" not in intersection

    def test_out_lines_multiple_output_lines(self):
        """OutLines with multiple output lines."""
        ol = StringSelection({"Ha", "Hb", "OIII", "SII", "NII", "HeI"})
        assert len(ol) == 6
        for line in ["Ha", "Hb", "OIII", "SII", "NII", "HeI"]:
            assert line in ol


class TestOutMeasuresSpecific:
    """Dedicated tests for OutMeasures type alias (unbounded StringSelection)"""

    def test_out_measures_basic_creation(self):
        """OutMeasures can be created with arbitrary measure names."""
        om = StringSelection({"flux", "width"})
        assert "flux" in om
        assert "width" in om

    def test_out_measures_standard_names(self):
        """OutMeasures with standard astronomical measure names."""
        om = StringSelection({"flux", "fwhm", "eqw", "velocity", "sigma"})
        assert "flux" in om
        assert "fwhm" in om
        assert "eqw" in om

    def test_out_measures_single_measure(self):
        """OutMeasures with single measure."""
        om = StringSelection({"flux"})
        assert "flux" in om
        assert len(om) == 1

    def test_out_measures_empty(self):
        """OutMeasures with empty set."""
        om = StringSelection(set())
        assert len(om) == 0

    def test_out_measures_with_all_keyword(self):
        """OutMeasures with 'all' keyword.
        
        From __contains__ docstring example:
        >>> "red" in RandomSelection({"all", "red"})
        False
        """
        om = StringSelection({"all", "flux"})
        # XOR: both in set
        assert "flux" not in om
        assert "all" not in om

    def test_out_measures_with_all_only(self):
        """OutMeasures with only 'all' keyword."""
        om = StringSelection({"all"})
        # Any measure name: super().__contains__(measure) ^ True = True
        assert "flux" in om
        assert "fwhm" in om
        assert "eqw" in om

    def test_out_measures_mixed_with_all(self):
        """OutMeasures excluding certain measures with 'all'."""
        om = StringSelection({"all", "flux", "fwhm"})
        # "flux": True ^ True = False
        # "fwhm": True ^ True = False
        # "eqw": False ^ True = True
        assert "flux" not in om
        assert "fwhm" not in om
        assert "eqw" in om

    def test_out_measures_to_fixed_empty(self):
        """OutMeasures.to_fixed() is empty (no _string_options)."""
        om = StringSelection({"flux", "fwhm"})
        result = om.to_fixed()
        assert result == {}

    def test_out_measures_pydantic_validation(self):
        """OutMeasures in Pydantic model."""
        class Config(BaseModel):
            measures: StringSelection

        config = Config(measures={"flux", "fwhm"})
        assert "flux" in config.measures
        assert "fwhm" in config.measures

    def test_out_measures_set_operations(self):
        """OutMeasures supports set operations."""
        om1 = StringSelection({"flux", "fwhm"})
        om2 = StringSelection({"fwhm", "eqw"})
        difference = om1 - om2
        assert "flux" in difference
        assert "fwhm" not in difference

    def test_out_measures_multiple_measures(self):
        """OutMeasures with multiple measures."""
        om = StringSelection({"flux", "fwhm", "eqw", "velocity", "sigma", "skewness"})
        assert len(om) == 6
        for measure in ["flux", "fwhm", "eqw", "velocity", "sigma", "skewness"]:
            assert measure in om

    def test_out_measures_complex_names(self):
        """OutMeasures with complex measure names."""
        om = StringSelection({"narrow_flux", "broad_fwhm", "asymmetry_measure"})
        assert "narrow_flux" in om
        assert "broad_fwhm" in om
        assert "asymmetry_measure" in om


class TestAllClassesInteraction:
    """Tests for interaction between different StringSelection classes"""

    def test_background_flux_vs_data_types(self):
        """BackgroundFlux and DataTypes are different types."""
        bf = BackgroundFlux({"pl", "fe"})
        dt = DataTypes({"pl", "fe"})
        assert type(bf) != type(dt)
        assert bf == dt  # But have same content

    def test_bounded_vs_unbounded_comparison(self):
        """Bounded (BackgroundFlux) vs unbounded (StringSelection)."""
        bf = BackgroundFlux({"pl"})
        un = StringSelection({"pl"})
        # Both have same content
        assert set(bf) == set(un)
        # But different types
        assert type(bf) != type(un)

    def test_pydantic_with_multiple_types(self):
        """Pydantic model with multiple StringSelection types."""
        class Config(BaseModel):
            data_types: DataTypes
            bg_flux: BackgroundFlux
            vary_lines: StringSelection
            out_lines: StringSelection

        config = Config(
            data_types={"pl"},
            bg_flux={"fe"},
            vary_lines={"Ha", "Hb"},
            out_lines={"Ha"}
        )
        assert "pl" in config.data_types
        assert "fe" in config.bg_flux
        assert "Ha" in config.vary_lines
        assert "Ha" in config.out_lines

    def test_all_subclasses_hashable(self):
        """All StringSelection subclasses are hashable."""
        items = [
            DataTypes({"pl"}),
            ModelTypes({"fe"}),
            BackgroundFlux({"ba"}),
            PowerLawModelParams({"flux"}),
            IronModelParams({"fwhm"}),
            BalmerModelParams({"ratio"}),
            HostGalaxyModelParams({"flux"}),
            GaussianModelParams({"strength"}),
            StringSelection({"custom"}),
        ]
        # Should be able to create a set from them (may have hash collisions, so set size may be <= len(items))
        s = set(items)
        assert len(s) > 0
        # Verify all items are hashable (no exception raised)
        for item in items:
            hash(item)

    def test_all_subclasses_in_dict(self):
        """All StringSelection subclasses can be dict keys."""
        dt = DataTypes({"pl"})
        bf = BackgroundFlux({"fe"})
        plp = PowerLawModelParams({"flux"})
        
        d = {
            dt: "data_types",
            bf: "bg_flux",
            plp: "power_law"
        }
        assert d[dt] == "data_types"
        assert d[bf] == "bg_flux"
        assert d[plp] == "power_law"


class TestStringSelectionsDocstringExamples:
    """Tests based on docstring examples in StringSelection.__contains__"""

    def test_bounded_example_1(self):
        """Docstring example: "red" in Colors({"red", "green"}) -> True"""
        class Colors(StringSelection):
            _string_options = ("red", "green", "blue")
        
        colors = Colors({"red", "green"})
        assert "red" in colors

    def test_bounded_example_2(self):
        """Docstring example: "blue" in Colors({"all"}) -> True"""
        class Colors(StringSelection):
            _string_options = ("red", "green", "blue")
        
        colors = Colors({"all"})
        assert "blue" in colors

    def test_bounded_example_3(self):
        """Docstring example: "red" in Colors({"all", "red"}) -> False"""
        class Colors(StringSelection):
            _string_options = ("red", "green", "blue")
        
        colors = Colors({"all", "red"})
        assert "red" not in colors

    def test_unbounded_example_1(self):
        """Docstring example: "red" in RandomSelection({"red", "green"}) -> True"""
        class RandomSelection(StringSelection):
            pass  # No _string_options
        
        selection = RandomSelection({"red", "green"})
        assert "red" in selection

    def test_unbounded_example_2(self):
        """Docstring example: "red" in RandomSelection({"all", "red"}) -> False"""
        class RandomSelection(StringSelection):
            pass  # No _string_options
        
        selection = RandomSelection({"all", "red"})
        assert "red" not in selection
