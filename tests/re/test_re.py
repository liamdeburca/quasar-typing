import pytest
import re
from pydantic import BaseModel, ValidationError, TypeAdapter

from quasar_typing.re import StrPattern


class TestStrPatternValidation:
    """Tests for StrPattern type - regex pattern validation"""

    def test_valid_simple_pattern(self):
        """Simple valid regex pattern."""
        adapter = TypeAdapter(StrPattern)
        result = adapter.validate_python(r"\d+")
        assert result == r"\d+"

    def test_valid_complex_pattern(self):
        """Complex valid regex pattern."""
        adapter = TypeAdapter(StrPattern)
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        result = adapter.validate_python(pattern)
        assert result == pattern

    def test_valid_pattern_with_groups(self):
        """Pattern with capture groups."""
        adapter = TypeAdapter(StrPattern)
        pattern = r"(\w+)\s+(\w+)"
        result = adapter.validate_python(pattern)
        assert result == pattern

    def test_valid_pattern_with_character_class(self):
        """Pattern with character class."""
        adapter = TypeAdapter(StrPattern)
        pattern = r"[a-z0-9]{3,}"
        result = adapter.validate_python(pattern)
        assert result == pattern

    def test_valid_pattern_with_quantifiers(self):
        """Pattern with quantifiers."""
        adapter = TypeAdapter(StrPattern)
        pattern = r"a{2,5}b+c*d?"
        result = adapter.validate_python(pattern)
        assert result == pattern

    def test_valid_empty_pattern(self):
        """Empty pattern is valid."""
        adapter = TypeAdapter(StrPattern)
        result = adapter.validate_python("")
        assert result == ""

    def test_valid_literal_pattern(self):
        """Literal string pattern."""
        adapter = TypeAdapter(StrPattern)
        result = adapter.validate_python("hello")
        assert result == "hello"

    def test_invalid_unmatched_bracket(self):
        """Pattern with unmatched bracket raises error."""
        adapter = TypeAdapter(StrPattern)
        with pytest.raises(ValidationError):
            adapter.validate_python(r"[a-z")

    def test_invalid_unmatched_paren(self):
        """Pattern with unmatched parenthesis raises error."""
        adapter = TypeAdapter(StrPattern)
        with pytest.raises(ValidationError):
            adapter.validate_python(r"(abc")

    def test_invalid_bad_escape(self):
        """Pattern with invalid escape sequence raises error."""
        adapter = TypeAdapter(StrPattern)
        with pytest.raises(ValidationError):
            adapter.validate_python(r"\k")

    def test_invalid_bad_quantifier(self):
        """Pattern with invalid quantifier raises error."""
        adapter = TypeAdapter(StrPattern)
        with pytest.raises(ValidationError):
            adapter.validate_python(r"*abc")

    def test_invalid_bad_repetition(self):
        """Pattern with bad repetition raises error."""
        adapter = TypeAdapter(StrPattern)
        with pytest.raises(ValidationError):
            adapter.validate_python(r"{3,1}")

    def test_pattern_in_pydantic_model(self):
        """StrPattern in Pydantic BaseModel."""
        class Config(BaseModel):
            pattern: StrPattern

        config = Config(pattern=r"\d{3}-\d{4}")
        assert config.pattern == r"\d{3}-\d{4}"

    def test_pattern_in_model_invalid(self):
        """Invalid pattern in model raises error."""
        class Config(BaseModel):
            pattern: StrPattern

        with pytest.raises(ValidationError):
            Config(pattern=r"[unclosed")

    def test_pattern_compiles(self):
        """Validated pattern can be compiled to regex."""
        adapter = TypeAdapter(StrPattern)
        pattern_str = adapter.validate_python(r"\w+@\w+\.\w+")
        regex = re.compile(pattern_str)
        assert regex.match("test@example.com") is not None

    def test_pattern_with_unicode(self):
        """Pattern with unicode characters."""
        adapter = TypeAdapter(StrPattern)
        pattern = r"[α-ω]+"
        result = adapter.validate_python(pattern)
        assert result == pattern

    def test_pattern_with_flags(self):
        """Pattern with inline flags."""
        adapter = TypeAdapter(StrPattern)
        pattern = r"(?i)hello"
        result = adapter.validate_python(pattern)
        assert result == pattern

    def test_pattern_with_lookahead(self):
        """Pattern with lookahead assertion."""
        adapter = TypeAdapter(StrPattern)
        pattern = r"foo(?=bar)"
        result = adapter.validate_python(pattern)
        assert result == pattern

    def test_pattern_with_lookbehind(self):
        """Pattern with lookbehind assertion."""
        adapter = TypeAdapter(StrPattern)
        pattern = r"(?<=foo)bar"
        result = adapter.validate_python(pattern)
        assert result == pattern

    def test_multiple_patterns_in_model(self):
        """Multiple StrPattern fields in model."""
        class Config(BaseModel):
            email: StrPattern
            phone: StrPattern
            url: StrPattern

        config = Config(
            email=r"\S+@\S+\.\S+",
            phone=r"\d{3}-\d{3}-\d{4}",
            url=r"https?://\S+"
        )
        assert config.email == r"\S+@\S+\.\S+"
        assert config.phone == r"\d{3}-\d{3}-\d{4}"
        assert config.url == r"https?://\S+"
