import pytest

class TestLogger:
    def test_multiprocessing_logger(self):
        from logging import getLogger
        from quasar_typing.logging import Logger_
        Logger_._validate(getLogger(__name__))