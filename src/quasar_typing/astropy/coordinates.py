__all__ = ["SkyCoordType"]

from astropy.coordinates.sky_coordinate import SkyCoord


class SkyCoordType(SkyCoord):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import PydanticCustomError
        from pydantic_core.core_schema import no_info_plain_validator_function

        from ..utils import isinstance_func

        def _validate(v: object):
            if isinstance(v, tuple):
                try:
                    return SkyCoord(*v)
                except Exception as exc:
                    raise PydanticCustomError(
                        "validation_error",
                        f"Could not create SkyCoord from tuple: {exc}",
                    ) from exc
            if isinstance(v, dict):
                try:
                    return SkyCoord(**v)
                except Exception as exc:
                    raise PydanticCustomError(
                        "validation_error",
                        f"Could not create SkyCoord from dict: {exc}",
                    ) from exc
            return isinstance_func(SkyCoord)(v)
        return no_info_plain_validator_function(_validate)