
from astropy.io import fits
from pydantic_core.core_schema import no_info_plain_validator_function

from ..utils import isinstance_func


class HDUListType(fits.HDUList):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(fits.HDUList)
        )


class PrimaryHDUType(fits.PrimaryHDU):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(fits.PrimaryHDU)
        )


class ImageHDUType(fits.ImageHDU):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(fits.ImageHDU)
        )


class BinTableHDUType(fits.BinTableHDU):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(fits.BinTableHDU)
        )