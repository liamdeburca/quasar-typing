__all__ = [
    "BinTableHDUType",
    "HDUListType",
    "ImageHDUType",
    "PrimaryHDUType"
]

from astropy.io.fits.hdu import BinTableHDU, HDUList, ImageHDU, PrimaryHDU
from pydantic_core.core_schema import no_info_plain_validator_function

from quasar_typing.utils import isinstance_func


class HDUListType(HDUList):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(HDUList)
        )


class PrimaryHDUType(PrimaryHDU):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(PrimaryHDU)
        )


class ImageHDUType(ImageHDU):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(ImageHDU)
        )


class BinTableHDUType(BinTableHDU):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(BinTableHDU)
        )