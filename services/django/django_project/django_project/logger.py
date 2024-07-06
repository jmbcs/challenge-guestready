import logging
from enum import Enum
from logging import Formatter, Logger, StreamHandler

import colorlog
from colorlog import ColoredFormatter
from pydantic import BaseModel


class LoggerLvl(str, Enum):
    CRITICAL = 'CRITICAL'
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    WARN = 'WARN'
    INFO = 'INFO'
    DEBUG = 'DEBUG'

    def lvl(self) -> int:
        """Return compatible python logging level"""
        return logging._nameToLevel[self.value]


class LoggerConfig(BaseModel):
    """Custom enumeration for logging levels with corresponding Python logging levels."""

    __DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    __DEFAULT_LOG_FORMAT = '%(levelname)-8s | %(asctime)s - %(name)s.%(funcName)s() - %(lineno)s | %(message)s'

    level: LoggerLvl
    log_format: str = __DEFAULT_LOG_FORMAT
    date_format: str = __DEFAULT_DATE_FORMAT
    enable_log_color: bool = False

    def configure_logger(self):
        """Configure the root logger based on the provided configuration."""
        logger: Logger = logging.getLogger()
        logger.setLevel(self.level.lvl())
        stream_handler: StreamHandler = logging.StreamHandler()
        if self.enable_log_color:
            __COLOR_LOG_FORMAT = '%(log_color)s%(levelname)-8s%(reset)s \033[0;34m|  %(asctime)s - %(name)s.%(funcName)s() - %(lineno)s |\033[0m %(message)s'
            self.log_format = __COLOR_LOG_FORMAT

            color_formatter: ColoredFormatter = colorlog.ColoredFormatter(
                self.log_format,
                log_colors={
                    'DEBUG': 'green',
                    'INFO': 'purple',
                    'WARNING': 'yellow',
                    'ERROR': 'bold_red',
                    'CRITICAL': 'bold_red,bg_white',
                },
                secondary_log_colors={},
                style='%',
                datefmt=self.date_format,
            )

            stream_handler.setFormatter(color_formatter)
        else:
            normal_formatter: Formatter = logging.Formatter(
                self.log_format, datefmt=self.date_format,
            )
            stream_handler.setFormatter(normal_formatter)

        logger.addHandler(stream_handler)
