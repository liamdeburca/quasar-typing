
from astropy import units
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import no_info_plain_validator_function

from ..utils import isinstance_func


class UnitType(units.Unit):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        def _validate(v: object):
            try:
                return units.Unit(v)
            except Exception as exc:
                raise PydanticCustomError(
                    "validation_error",
                    f"Could not convert to Unit: {exc}",
                ) from exc
        return no_info_plain_validator_function(_validate)

    
class CompositeUnitType(units.CompositeUnit):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        def _validate(v: object):
            if isinstance(v, units.CompositeUnit):
                return v

            try:
                return units.CompositeUnit(v)
            except Exception as exc:
                raise PydanticCustomError(
                    "validation_error",
                    f"Could not convert to CompositeUnit: {exc}",
                ) from exc
        return no_info_plain_validator_function(_validate)


class QuantityType(units.Quantity):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return no_info_plain_validator_function(
            isinstance_func(units.Quantity),
        )
