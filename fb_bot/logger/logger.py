import inspect
import sys
from datetime import datetime

import logging

import json_log_formatter

from highlights import settings


class LoggerWrapper:
    def __init__(self):
        self.logger = logging.getLogger('logger')
        self.logger.setLevel(logging.INFO)

        # Stdout
        formatter = json_log_formatter.JSONFormatter()
        stream_handler = logging.StreamHandler(sys.stdout)

        if not settings.DEBUG:
            stream_handler.setFormatter(formatter)

        self.logger.addHandler(stream_handler)

        self.enabled = True

    def log(self, message, level, extra, show_error_stack=True):
        if not self.enabled:
            return

        # Add stack trace if error or critical
        exc_info = level in [logging.ERROR, logging.CRITICAL] and show_error_stack

        # Add level field to determine log level
        level_name = logging.getLevelName(level)
        extra['level'] = level_name

        # Add time to log
        time = datetime.utcnow()
        extra['time'] = time

        # Add caller info
        func_info = inspect.stack()[2]  # Go back 2 time backward the call stack to get original function call
        extra['function_filename'] = func_info.filename
        extra['function_name'] = func_info.function
        extra['function_position'] = func_info.lineno

        # Add level in message
        message = '{} [{}] {}'.format(level_name, time, message)

        self.logger.log(level, message, exc_info=exc_info, extra=extra)

        # Show in debug the params
        if settings.DEBUG:
            self.logger.log(level, '{} [{}] {}'.format(level_name, time, str(extra)))

    def is_enabled(self):
        return self.enabled

    def disable(self):
        self.enabled = False


LOGGER = LoggerWrapper()


def disable():
    LOGGER.disable()


# Deprecated - use more specific methods
def log(message, forward=False):
    LOGGER.log(message, logging.INFO, {})


def info(message, extra={}):
    LOGGER.log(message, logging.INFO, extra)


def warning(message, extra={}):
    LOGGER.log(message, logging.WARNING, extra)


def error(message, extra={}):
    LOGGER.log(message, logging.ERROR, extra)


def critical(message, extra={}):
    LOGGER.log(message, logging.CRITICAL, extra)


def log_for_user(message, user_id, extra={}):
    extra['user_id'] = user_id
    LOGGER.log(message, logging.INFO, extra)


def log_error_for_user(message, user_id, extra={}):
    extra['user_id'] = user_id
    LOGGER.log(message, logging.ERROR, extra, show_error_stack=False)