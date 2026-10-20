__all__ = ["CompositeUnitType", "QuantityType", "UnitType"]

from astropy.units.core import CompositeUnit, Unit
from astropy.units.quantity import Quantity

from ..utils import isinstance_func


class UnitType(Unit):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import PydanticCustomError
        from pydantic_core.core_schema import no_info_plain_validator_function

        def _validate(v: object):
            try:
                return Unit(v)
            except Exception as exc:
                raise PydanticCustomError(
                    "validation_error",
                    f"Could not convert to Unit: {exc}",
                ) from exc
        return no_info_plain_validator_function(_validate)

    
class CompositeUnitType(CompositeUnit):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import PydanticCustomError
        from pydantic_core.core_schema import no_info_plain_validator_function

        def _validate(v: object):
            if isinstance(v, CompositeUnit):
                return v

            try:
                return CompositeUnit(v)
            except Exception as exc:
                raise PydanticCustomError(
                    "validation_error",
                    f"Could not convert to CompositeUnit: {exc}",
                ) from exc
        return no_info_plain_validator_function(_validate)


class QuantityType(Quantity):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core.core_schema import no_info_plain_validator_function
        return no_info_plain_validator_function(
            isinstance_func(Quantity),
        )
