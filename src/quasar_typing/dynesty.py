__all__ = [
    "DynamicNestedSamplerType",
    "SamplerType",
]

from importlib import import_module

try:
    import_module("dynesty")
except ImportError as exc:
    msg = "Must install 'dynesty' to use 'quasar_typing.dynesty'"
    raise ImportError(msg) from exc

### 

import dynesty

from .utils import isinstance_func


class SamplerType(dynesty.sampler.Sampler):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core.core_schema import no_info_plain_validator_function
        return no_info_plain_validator_function(
            isinstance_func(dynesty.sampler.Sampler)
        )


class DynamicNestedSamplerType(dynesty.DynamicNestedSampler):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core.core_schema import no_info_plain_validator_function
        return no_info_plain_validator_function(
            isinstance_func(dynesty.DynamicNestedSampler)
        )
