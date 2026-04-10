from typing import Literal, Self
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

class StringSelection(frozenset[Literal['all'] | str]):
    """
    frozenset[Literal['all'] | str]

    Notes
    -----
    Selection of strings. If 'all' is included, all except the specified strings 
    are selected instead.
    """
    @classmethod
    def _validate(cls, value: object) -> Self:
        if not isinstance(value, (frozenset, set, list, tuple)):
            msg = f"Expected a valid iterable, got {type(value).__name__}"
            raise PydanticCustomError(msg, type=value)
        if not all(isinstance(item, str) for item in value):
            msg = "Expected all items to be strings"
            raise PydanticCustomError(msg, type=value)
        return frozenset(value)
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)
    
    def __call__(self, string: str) -> bool:
        """
        Whether to vary the given string or not. 
        """
        return ('all' in self) ^ (string in self)