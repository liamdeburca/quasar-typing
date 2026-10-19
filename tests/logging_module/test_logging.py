import pytest
import logging
from io import StringIO
from pydantic import BaseModel, ValidationError, TypeAdapter, ConfigDict

from quasar_typing.logging import LoggerType, FileHandlerType


class TestLoggerTypeWithArbitraryTypes:
    """Tests for LoggerType - logging.Logger validation with arbitrary_types_allowed=True"""

    def test_logger_type_accepts_logger(self):
        """LoggerType accepts a logging.Logger instance."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            logger: LoggerType

        logger = logging.getLogger("test_logger")
        config = Config(logger=logger)
        assert isinstance(config.logger, logging.Logger)
        assert config.logger is logger

    def test_logger_type_accepts_root_logger(self):
        """LoggerType accepts the root logger."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            logger: LoggerType

        root_logger = logging.getLogger()
        config = Config(logger=root_logger)
        assert isinstance(config.logger, logging.Logger)
        assert config.logger is root_logger

    def test_logger_type_rejects_none(self):
        """LoggerType rejects None."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            logger: LoggerType

        with pytest.raises(ValidationError):
            Config(logger=None)

    def test_logger_type_rejects_string(self):
        """LoggerType rejects string."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            logger: LoggerType

        with pytest.raises(ValidationError):
            Config(logger="not a logger")

    def test_logger_type_rejects_int(self):
        """LoggerType rejects integer."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            logger: LoggerType

        with pytest.raises(ValidationError):
            Config(logger=42)

    def test_logger_type_rejects_handler(self):
        """LoggerType rejects logging.Handler."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            logger: LoggerType

        handler = logging.StreamHandler()
        with pytest.raises(ValidationError):
            Config(logger=handler)

    def test_logger_type_rejects_file_handler(self):
        """LoggerType rejects logging.FileHandler."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            logger: LoggerType

        handler = logging.FileHandler("/tmp/test.log")
        try:
            with pytest.raises(ValidationError):
                Config(logger=handler)
        finally:
            handler.close()

    def test_logger_type_with_multiple_loggers(self):
        """LoggerType validates multiple different loggers."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            logger1: LoggerType
            logger2: LoggerType

        logger1 = logging.getLogger("logger1")
        logger2 = logging.getLogger("logger2")
        
        config = Config(logger1=logger1, logger2=logger2)
        assert config.logger1 is logger1
        assert config.logger2 is logger2

    def test_logger_type_passthrough(self):
        """Validated logger is the same instance (passthrough)."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            logger: LoggerType

        logger = logging.getLogger("passthrough_test")
        config = Config(logger=logger)
        assert config.logger is logger

    def test_logger_type_with_handlers(self):
        """LoggerType accepts logger with handlers."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            logger: LoggerType

        logger = logging.getLogger("test_with_handlers")
        handler = logging.StreamHandler()
        logger.addHandler(handler)
        
        config = Config(logger=logger)
        assert isinstance(config.logger, logging.Logger)
        assert config.logger is logger
        
        logger.removeHandler(handler)


class TestFileHandlerTypeWithArbitraryTypes:
    """Tests for FileHandlerType - logging.FileHandler validation with arbitrary_types_allowed=True"""

    def test_file_handler_type_accepts_file_handler(self):
        """FileHandlerType accepts a logging.FileHandler instance."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            handler: FileHandlerType

        handler = logging.FileHandler("/tmp/test.log")
        try:
            config = Config(handler=handler)
            assert isinstance(config.handler, logging.FileHandler)
            assert config.handler is handler
        finally:
            handler.close()

    def test_file_handler_type_rejects_none(self):
        """FileHandlerType rejects None."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            handler: FileHandlerType

        with pytest.raises(ValidationError):
            Config(handler=None)

    def test_file_handler_type_rejects_string(self):
        """FileHandlerType rejects string."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            handler: FileHandlerType

        with pytest.raises(ValidationError):
            Config(handler="not a file handler")

    def test_file_handler_type_rejects_int(self):
        """FileHandlerType rejects integer."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            handler: FileHandlerType

        with pytest.raises(ValidationError):
            Config(handler=42)

    def test_file_handler_type_rejects_logger(self):
        """FileHandlerType rejects logging.Logger."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            handler: FileHandlerType

        logger = logging.getLogger("test")
        with pytest.raises(ValidationError):
            Config(handler=logger)

    def test_file_handler_type_rejects_stream_handler(self):
        """FileHandlerType rejects logging.StreamHandler."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            handler: FileHandlerType

        handler = logging.StreamHandler()
        with pytest.raises(ValidationError):
            Config(handler=handler)

    def test_file_handler_type_passthrough(self):
        """Validated handler is the same instance (passthrough)."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            handler: FileHandlerType

        handler = logging.FileHandler("/tmp/test.log")
        try:
            config = Config(handler=handler)
            assert config.handler is handler
        finally:
            handler.close()

    def test_file_handler_type_with_formatter(self):
        """FileHandlerType accepts handler with formatter."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            handler: FileHandlerType

        handler = logging.FileHandler("/tmp/test.log")
        formatter = logging.Formatter("%(asctime)s - %(message)s")
        handler.setFormatter(formatter)
        
        try:
            config = Config(handler=handler)
            assert isinstance(config.handler, logging.FileHandler)
            assert config.handler.formatter is formatter
        finally:
            handler.close()

    def test_file_handler_type_multiple_handlers(self):
        """FileHandlerType validates multiple handlers."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            handler1: FileHandlerType
            handler2: FileHandlerType

        handler1 = logging.FileHandler("/tmp/test1.log")
        handler2 = logging.FileHandler("/tmp/test2.log")
        
        try:
            config = Config(handler1=handler1, handler2=handler2)
            assert config.handler1 is handler1
            assert config.handler2 is handler2
        finally:
            handler1.close()
            handler2.close()

    def test_logger_and_file_handler_together(self):
        """Logger and FileHandler can be used together in model."""
        class Config(BaseModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            logger: LoggerType
            handler: FileHandlerType

        logger = logging.getLogger("test_combined")
        handler = logging.FileHandler("/tmp/test.log")
        
        try:
            config = Config(logger=logger, handler=handler)
            assert isinstance(config.logger, logging.Logger)
            assert isinstance(config.handler, logging.FileHandler)
        finally:
            handler.close()
