from logging import FileHandler

from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function


class FileHandler_(FileHandler):
    """
    logging.FileHandler
    """

    @classmethod
    def _validate(cls, value: object) -> FileHandler:
        if not isinstance(value, FileHandler):
            msg = f"Expected logging.FileHandler, got {type(value).__name__}"
            raise PydanticCustomError("validation_error", msg)
        return value

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(cls._validate)

    def __getstate__(self) -> dict:
        return {
            "filename": self.baseFilename,
            "mode": self.mode,
            "encoding": self.encoding,
            "delay": self.delay,
            "level": self.level,
            "errors": self.errors,
        }

    def __setstate__(self, state: dict) -> None:
        self.__init__(
            filename=state["filename"],
            mode=state["mode"],
            encoding=state["encoding"],
            delay=state["delay"],
            errors=state["errors"],
        )
        self.setLevel(state["level"])
