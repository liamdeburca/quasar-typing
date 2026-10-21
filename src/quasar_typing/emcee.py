__all__ = [
    "BackendType",
    "EnsembleSamplerType",
    "HDFBackendType",
    "MoveType"
]

from importlib import import_module

import_module("emcee")

from typing import Annotated

from emcee.backends.backend import Backend
from emcee.backends.hdf import HDFBackend
from emcee.ensemble import EnsembleSampler
from emcee.moves.move import Move
from pydantic_core.core_schema import no_info_plain_validator_function

from quasar_typing.utils import isinstance_func, isinstance_validator


class MoveType(Move):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(Move)
        )


class EnsembleSamplerType(EnsembleSampler):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(EnsembleSampler)
        )


class BackendType(Backend):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(Backend)
        )


type HDFBackendType = Annotated[BackendType, isinstance_validator(HDFBackend)]