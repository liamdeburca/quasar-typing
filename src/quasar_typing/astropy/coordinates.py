from astropy import coordinates
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

from ..utils import isinstance_func


class SkyCoordType(coordinates.SkyCoord):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        def _validate(v: object):
            if isinstance(v, tuple):
                try:
                    return coordinates.SkyCoord(*v)
                except Exception as exc:
                    raise PydanticCustomError(
                        "validation_error",
                        f"Could not create SkyCoord from tuple: {exc}",
                    ) from exc
            if isinstance(v, dict):
                try:
                    return coordinates.SkyCoord(**v)
                except Exception as exc:
                    raise PydanticCustomError(
                        "validation_error",
                        f"Could not create SkyCoord from dict: {exc}",
                    ) from exc
            return isinstance_func(coordinates.SkyCoord)(v)
        return no_info_plain_validator_function(_validate)