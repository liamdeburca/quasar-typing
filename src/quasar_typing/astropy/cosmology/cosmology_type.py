__all__ = ["CosmologyType"]

from astropy.cosmology import Cosmology
from pydantic_core.core_schema import no_info_plain_validator_function

from quasar_typing.utils import isinstance_func


class CosmologyType(Cosmology):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(Cosmology)
        )
