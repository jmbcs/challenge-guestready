import logging
from unittest import mock

import pytest
from api.logger import LoggerConfig, LoggerLvl
from colorlog import ColoredFormatter


@pytest.fixture
def reset_logging():
    """
    Fixture to reset logging configuration after each test.
    This ensures that changes made to the logging configuration in one test
    do not affect other tests.
    """
    yield
    # Reset logging handlers and level after each test
    logging.getLogger().handlers = []  # Reset handlers
    logging.getLogger().setLevel(logging.NOTSET)  # Reset level


def test_logger_level(reset_logging):
    """
    Test that the LoggerConfig class correctly sets the logging level.
    """
    with mock.patch("logging.getLogger") as mock_get_logger:
        mock_logger = mock.Mock()
        mock_get_logger.return_value = mock_logger

        # Create LoggerConfig instance with log level set to DEBUG
        config = LoggerConfig(level=LoggerLvl.DEBUG)
        config.configure_logger()

        # Assert that getLogger was called once
        mock_get_logger.assert_called_once_with()
        # Assert that the log level was set to DEBUG
        mock_logger.setLevel.assert_called_once_with(logging.DEBUG)


def test_logger_format(reset_logging):
    """
    Test that the LoggerConfig class correctly sets the log format.
    """
    custom_format = "%(name)s - %(levelname)s - %(message)s"
    with mock.patch("logging.getLogger") as mock_get_logger:
        mock_logger = mock.Mock()
        mock_get_logger.return_value = mock_logger

        # Create LoggerConfig instance with log level set to INFO and custom log format
        config = LoggerConfig(level=LoggerLvl.INFO, log_format=custom_format)
        config.configure_logger()

        # Assert that getLogger was called once
        mock_get_logger.assert_called_once_with()
        # Retrieve the stream handler added to the logger
        stream_handler = mock_logger.addHandler.call_args[0][0]
        # Assert that the stream handler uses the correct formatter
        assert isinstance(stream_handler.formatter, logging.Formatter)
        assert stream_handler.formatter._fmt == custom_format


def test_colored_formatter_enabled(reset_logging):
    """
    Test that the LoggerConfig class uses ColoredFormatter when color logging is enabled.
    """
    with mock.patch("logging.getLogger") as mock_get_logger:
        mock_logger = mock.Mock()
        mock_get_logger.return_value = mock_logger

        # Create LoggerConfig instance with log level set to WARNING and color logging enabled
        config = LoggerConfig(level=LoggerLvl.WARNING, enable_log_color=True)
        config.configure_logger()

        # Assert that getLogger was called once
        mock_get_logger.assert_called_once_with()
        # Retrieve the stream handler added to the logger
        stream_handler = mock_logger.addHandler.call_args[0][0]
        # Assert that the stream handler uses ColoredFormatter
        assert isinstance(stream_handler.formatter, ColoredFormatter)


def test_colored_formatter_disabled(reset_logging):
    """
    Test that the LoggerConfig class uses logging.Formatter when color logging is disabled.
    """
    with mock.patch("logging.getLogger") as mock_get_logger:
        mock_logger = mock.Mock()
        mock_get_logger.return_value = mock_logger

        # Create LoggerConfig instance with log level set to ERROR and color logging disabled
        config = LoggerConfig(level=LoggerLvl.ERROR, enable_log_color=False)
        config.configure_logger()

        # Assert that getLogger was called once
        mock_get_logger.assert_called_once_with()
        # Retrieve the stream handler added to the logger
        stream_handler = mock_logger.addHandler.call_args[0][0]
        # Assert that the stream handler uses logging.Formatter
        assert isinstance(stream_handler.formatter, logging.Formatter)
        # Assert that the stream handler does not use ColoredFormatter
        assert not isinstance(stream_handler.formatter, ColoredFormatter)
