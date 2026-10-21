__all__ = [
    "DynamicNestedSamplerType",
    "SamplerType",
]

from importlib import import_module

import_module("dynesty")

import dynesty
from pydantic_core.core_schema import no_info_plain_validator_function

from quasar_typing.utils import isinstance_func


class SamplerType(dynesty.sampler.Sampler):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(dynesty.sampler.Sampler)
        )


class DynamicNestedSamplerType(dynesty.DynamicNestedSampler):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(dynesty.DynamicNestedSampler)
        )
