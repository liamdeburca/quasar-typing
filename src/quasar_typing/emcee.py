__all__ = [
    "BackendType",
    "EnsembleSamplerType",
    "HDFBackendType",
    "MoveType"
]

from importlib import import_module

try:
    import_module("emcee")
except ImportError as exc:
    msg = "Must install 'emcee' to use 'quasar_typing.emcee'"
    raise ImportError(msg) from exc

### Pydantic type wrappers for emcee classes

from typing import Annotated

from emcee import EnsembleSampler, backends, moves
from pydantic_core.core_schema import no_info_plain_validator_function

from .utils import isinstance_func, isinstance_validator


class MoveType(moves.Move):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(moves.Move)
        )


class EnsembleSamplerType(EnsembleSampler):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(EnsembleSampler)
        )


class BackendType(backends.Backend):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(backends.Backend)
        )


type HDFBackendType = Annotated[
    BackendType,
    isinstance_validator(backends.HDFBackend),
]