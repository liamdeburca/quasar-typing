__all__ = [
    'StringSelection',
]

from typing import Literal, TypeVar, get_args, Self
from pydantic import validate_call
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

T = TypeVar('T', bound=str)

class StringSelection(set[T]):
    """
    set[T]

    Notes
    -----
    Selection of strings. If 'all' is included, all except the specified strings 
    are selected instead using the class' `_string_options` attribute.

    Coercion
    --------
    - Any iterable of strings is treated as a set of strings
    """
    _string_options: tuple[str, ...] = tuple()

    @validate_call
    def __init__(self, selection: set[Literal['all'] | T]):
        """
        ** PYDANTIC VALIDATED METHOD **
        """
        self._all_in_initial_selection: bool = ('all' in selection)
        super().__init__(
            s
            for s in self._string_options
            if self._all_in_initial_selection ^ (s in selection)
        )

    @classmethod
    def _validate(cls, value: object) -> Self:
        if isinstance(value, StringSelection):
            return value
        
        try:
            return cls(value or {'all'})
        except Exception as _:
            msg = f"Could not coerce value to set: {value}"
            raise PydanticCustomError('validation_error', msg)

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)
        
    @classmethod
    def __class_getitem__(cls, params):
        string_options = tuple(get_args(params))

        class TypedStringSelection(StringSelection):
            _string_options = string_options

        return TypedStringSelection
    
    def __call__(self, s: str) -> bool:
        """
        Checks whether a string is in the selection.

        Notes
        -----
        This should only be used 'VaryLines' / 'OutMeasures' / 'OutLines' as the 
        options are not necessarily known at runtime. 

        In other cases, use 's in string_selection'.
        """
        return self._all_in_initial_selection ^ (s in self)

    def __hash__(self) -> int:
        return hash(frozenset(self))