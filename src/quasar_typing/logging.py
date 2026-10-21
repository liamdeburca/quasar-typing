import logging

from pydantic_core.core_schema import no_info_plain_validator_function

from quasar_typing.utils import isinstance_func


class LoggerType(logging.Logger):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(logging.Logger)
        )

class FileHandlerType(logging.FileHandler):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(logging.FileHandler)
        )