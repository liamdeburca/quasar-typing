__all__ = [
    "BackgroundFlux",
    "BalmerModelParams",
    "DataTypes",
    "GaussianModelParams",
    "HostGalaxyModelParams",
    "IronModelParams",
    "ModelTypes",
    "OutLines",
    "OutMeasures",
    "PowerLawModelParams",
    "StringSelection",
    "VaryLines",
]

from typing import Literal, Self, TypeVar

from pydantic import validate_call

T = TypeVar("T", bound=str)


class StringSelection(set[Literal["all"] | T]):
    """
    Set of string values. 

    If the _string_options attribute is defined, only strings from this set are 
    considered valid, and if `all` is included, all except the specified strings 
    are selected instead.

    Otherwise, this class acts as a regular set of strings. 

    Examples
    --------
    class Colors(StringSelection[Literal["red", "green", "blue"]]):
        _string_options = ("red", "green", "blue")

    >>> Colors({"red", "green"})
    Colors({"red", "green"})
    >>> Colors({"all"})
    Colors({"red", "green", "blue"})
    >>> Colors({"all", "red"})
    Colors({"green", "blue"})
    """
    _string_options: tuple[T, ...] = ()

    @validate_call
    def __init__(self, selection: set[Literal["all"] | T]):
        self._contains_all: bool = "all" in selection

        if self._string_options:
            super().__init__(
                s
                for s in self._string_options
                if self._contains_all ^ (s in selection)
            )
        else:
            super().__init__(selection)


    def __contains__(self, s: object) -> bool:
        """
        Check if the string `s` is considered part of the selection, taking into 
        account the "all" option.

        Examples
        --------
        ```python
        class Colors(StringSelection[Literal["red", "green", "blue"]]):
            _string_options = ("red", "green", "blue")

        >>> "red" in Colors({"red", "green"})
        True
        >>> "blue" in Colors({"all"})
        True
        >>> "red" in Colors({"all", "red"})
        False

        class RandomSelection(StringSelection[str]):
            "No string options"

        >>> "red" in RandomSelection({"red", "green"})
        True
        >>> "red" in RandomSelection({"all", "red"})
        False
        ```
        """
        return super().__contains__(s) ^ super().__contains__("all")


    @classmethod
    def _validate(cls, value: object) -> Self:
        from pydantic_core import PydanticCustomError
        if isinstance(value, StringSelection):
            return cls(value)

        try:
            return cls(value or {"all"})
        except ValueError:
            raise PydanticCustomError(
                "validation_error", 
                "Could not coerce value to set: {value}",
                {"value": value},
            )

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core.core_schema import no_info_plain_validator_function
        return no_info_plain_validator_function(cls._validate)

    def __call__(self, s: T) -> bool:
        raise DeprecationWarning(
            "` __call__` is deprecated: use 's in string_selection' instead."
        )

    def __hash__(self) -> int:
        return hash(frozenset(self))

    def to_fixed(self) -> dict[T, bool]:
        return {
            s: (s in self) 
            for s in self._string_options
        }


class DataTypes(StringSelection[Literal["pl", "fe", "ba", "hg", "em"]]):
    _string_options = ("pl", "fe", "ba", "hg", "em")


class ModelTypes(StringSelection[Literal["pl", "fe", "ba", "hg", "em"]]):
    _string_options = ("pl", "fe", "ba", "hg", "em")


class BackgroundFlux(StringSelection[Literal["pl", "fe", "ba", "hg", "em"]]):
    _string_options = ("pl", "fe", "ba", "hg", "em")


class VaryLines(StringSelection[str]):
    pass

class OutLines(StringSelection[str]):
    pass

class OutMeasures(StringSelection[str]):
    pass


class PowerLawModelParams(StringSelection[Literal["flux", "alpha"]]):
    _string_options = ("flux", "alpha")


class IronModelParams(StringSelection[Literal["flux", "fwhm", "split", "left", "right"]]):
    _string_options = ("flux", "fwhm", "split", "left", "right")


class BalmerModelParams(StringSelection[Literal["flux", "fwhm", "ratio"]]):
    _string_options = ("flux", "fwhm", "ratio")


class HostGalaxyModelParams(StringSelection[Literal["flux", "fwhm"]]):
    _string_options = ("flux", "fwhm")


class GaussianModelParams(StringSelection[Literal["strength", "fwhm_v", "v_off"]]):
    _string_options = ("strength", "fwhm_v", "v_off")

