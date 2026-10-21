import re
from typing import Annotated

from pydantic_core import PydanticCustomError

from quasar_typing.utils import after_validator_decorator


@after_validator_decorator
def validate_is_valid_pattern(s: str) -> str:
    try:
        re.compile(s)
    except re.error:
        raise PydanticCustomError(
            "validation_error",
            "String could not be compiled as a valid regular expression pattern"
        )
    return s

type StrPattern = Annotated[str, validate_is_valid_pattern]