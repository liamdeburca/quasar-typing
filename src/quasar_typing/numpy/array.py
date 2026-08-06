from typing import ClassVar, Self

from numpy import array, invert, isfinite, issubdtype, ndarray, sort
from numpy.typing import NDArray
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import (
    no_info_plain_validator_function,
)


class Array_(NDArray):
    """
    numpy.ndarray

    Base class for type-validated numpy arrays with automatic coercion
    and constraint checking (dtype, shape, finite values, etc.).
    """
    _coerce: ClassVar[bool]

    _dtype: ClassVar[type | None] = None
    _ndim: ClassVar[int | None] = None

    _check_finite: ClassVar[bool] = False
    _check_has_elements: ClassVar[bool] = False
    _check_is_sorted: ClassVar[bool] = False

    @classmethod
    def _validate_ndarray(cls, value: object) -> ndarray:
        msg = f"{cls.__doc__} // "
        if not isinstance(value, ndarray):
            if cls._coerce:
                try:
                    value = array(
                        value,
                        dtype=cls._dtype,
                        ndmin=cls._ndim or 0,
                    )
                except Exception as e:
                    msg += f"Failed to coerce value to numpy array: {e}"
                    raise PydanticCustomError("validation_error", msg)
            else:
                msg += f"Expected numpy array, got {type(value)}"
                raise PydanticCustomError("validation_error", msg)

        return value

    @classmethod
    def _validate_dtype(cls, value: ndarray) -> ndarray:
        msg = f"{cls.__doc__} // "
        if not issubdtype(value.dtype, cls._dtype):
            if cls._coerce:
                try:
                    value = value.astype(cls._dtype)
                except Exception as e:
                    msg += f"Failed to coerce value to numpy array of dtype {cls._dtype}: {e}"
                    raise PydanticCustomError("validation_error", msg)
            else:
                msg += f"Expected numpy array of dtype {cls._dtype}, "\
                    f"got {value.dtype}"
                raise PydanticCustomError("validation_error", msg)

        return value

    @classmethod
    def _validate_ndim(cls, value: ndarray) -> ndarray:
        msg = f"{cls.__doc__} // "
        if value.ndim != cls._ndim:
            if cls._coerce:
                try:
                    value = value.reshape((-1,) * cls._ndim)
                except Exception as e:
                    msg += f"Failed to coerce value to numpy array of ndim {cls._ndim}: {e}"
                    raise PydanticCustomError("validation_error", msg)
            else:
                msg += f"Expected numpy array of ndim {cls._ndim}, "\
                    f"got {value.ndim}"
                raise PydanticCustomError("validation_error", msg)

        return value

    @classmethod
    def _validate_finite(cls, value: ndarray) -> ndarray:
        msg = f"{cls.__doc__} // "
        if not (mask := isfinite(value)).all():
            non_finite_count: int = invert(mask).sum()
            msg += f"Expected numpy array with finite values, "\
                f"got array with {non_finite_count} non-finite values"
            raise PydanticCustomError("validation_error", msg)
        return value

    @classmethod
    def _validate_has_elements(cls, value: ndarray) -> ndarray:
        msg = f"{cls.__doc__} // "
        if not value.size > 0:
            msg += "Expected numpy array with at least one element, "\
                "got an empty array"
            raise PydanticCustomError("validation_error", msg)
        return value

    @classmethod
    def _validate_is_sorted(cls, value: ndarray) -> ndarray:
        msg = f"{cls.__doc__} // "
        if not (value[:-1] <= value[1:]).all():
            if cls._coerce:
                try:
                    value = sort(value, axis=-1)
                except Exception as e:
                    msg += f"Failed to coerce value to sorted numpy array: {e}"
                    raise PydanticCustomError("validation_error", msg)
            else:
                msg += "Expected numpy array sorted in non-descending order, "\
                    "got unsorted array"
                raise PydanticCustomError("validation_error", msg)
        return value

    @classmethod
    def _validate(cls, value: object) -> Self:
        value = cls._validate_ndarray(value)
        if cls._dtype is not None:
            value = cls._validate_dtype(value)
        if cls._ndim is not None:
            value = cls._validate_ndim(value)
        if cls._check_finite:
            value = cls._validate_finite(value)
        if cls._check_has_elements:
            value = cls._validate_has_elements(value)
        if cls._check_is_sorted:
            value = cls._validate_is_sorted(value)
        return value

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)
