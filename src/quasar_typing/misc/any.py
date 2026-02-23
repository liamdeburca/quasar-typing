from logging import Logger
from pydantic_core import PydanticCustomError

class AnyTypeGenerator:

    def __class_getitem__(*params):
        _cls_types = params

        if not isinstance(_cls_types, tuple):
            _cls_types = (_cls_types,)

        class AnyType(*_cls_types):
            cls_types: tuple = _cls_types

            @classmethod
            def __get_validators__(cls):
                yield cls.validate

            @classmethod
            def validate(cls, value, _info):
                if not isinstance(value, cls.cls_types):
                    msg = "Input must be of type '{}', but is '{}'!"\
                        .format(
                            cls.cls_types,
                            type(value).__name__,
                        )
                    raise PydanticCustomError('validation_error', msg)

                return value
            
        return AnyType

class AnyModelGenerator:

    def __class_getitem__(cls, model_name):
        _model_name: str = model_name

        class AnyModel:
            model_name: str = _model_name

            @classmethod
            def __get_validators__(cls):
                yield cls.validate

            @classmethod
            def validate(cls, value, _info):
                value_name = value.__class__.name

                if not (value_name == cls.model_name):
                    msg = "Input must be of type '{}', but is '{}'!" \
                        .format(cls.model_name, value_name)
                    raise PydanticCustomError('validation_error', msg)

                return value
            
        return AnyModel