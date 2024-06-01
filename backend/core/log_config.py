import logging
import sys
from logging.handlers import TimedRotatingFileHandler

from backend.core.config import BASE_DIR


class ExcludeLoggerFilter(logging.Filter):
    def __init__(self, exclude_logger_name):
        self.exclude_logger_name = exclude_logger_name

    def filter(self, record):
        return self.exclude_logger_name not in record.name


class ColoredFormatter(logging.Formatter):
    grey = "\x1b[90m"  # Серый
    green = "\x1b[92m"  # Зеленый
    yellow = "\x1b[93m"  # Желтый
    red = "\x1b[91m"  # Красный
    bold_red = "\x1b[91;1m"  # Жирный красный
    reset = "\x1b[0m"  # Сброс цвета
    format = "[{asctime}] #{levelname:8} | in: {filename}:{lineno}:{funcName} | fr: {name} | m: {message}"
    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, style="{", datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


class PlainFormatter(logging.Formatter):
    format = "[{asctime}] #{levelname:8} | in: {filename}:{lineno}:{funcName} | fr: {name} | m: {message}"
    FORMATS = {
        logging.DEBUG: format,
        logging.INFO: format,
        logging.WARNING: format,
        logging.ERROR: format,
        logging.CRITICAL: format,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, style="{", datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


class CustomLoggerConfig:
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        # Create a console handler
        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.stream_handler.setFormatter(ColoredFormatter())

        # Create a file handler with timed rotation
        self.file_handler = TimedRotatingFileHandler(
            BASE_DIR / "logs" / "backend logs/app.log",
            when="midnight",
            backupCount=0,
            encoding="utf-8",
        )
        self.file_handler.setFormatter(PlainFormatter())

        self.exclude_filter = ExcludeLoggerFilter("watchfiles.main")
        self.stream_handler.addFilter(self.exclude_filter)
        self.file_handler.addFilter(self.exclude_filter)

        self.logger.addHandler(self.stream_handler)
        self.logger.addHandler(self.file_handler)

    def get_logger(self, name=None):
        if name:
            return self.logger.getChild(name)
        return self.logger


custom_logger_config = CustomLoggerConfig()
root_logger = custom_logger_config.get_logger()
get_logger = custom_logger_config.get_logger
