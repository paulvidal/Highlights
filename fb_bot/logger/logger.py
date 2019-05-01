import sys
from datetime import datetime

from logentries import LogentriesHandler
import logging

import json_log_formatter

from highlights import settings


class LoggerWrapper:
    def __init__(self):
        self.logger = logging.getLogger('logentries')
        self.logger.setLevel(logging.INFO)

        # Logentries
        logentries_token = settings.get_env_var("LOGENTRIES_TOKEN")
        self.logger.addHandler(LogentriesHandler(logentries_token))

        # Stdout
        formatter = json_log_formatter.JSONFormatter()
        stream_handler = logging.StreamHandler(sys.stdout)
        if not settings.DEBUG:
            stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        self.enabled = True

    def log(self, message, level, extra):
        if not self.enabled:
            return

        # Add stack trace if error or critical
        exc_info = level in [logging.ERROR, logging.CRITICAL]

        # Add level field to determine log level
        level_name = logging.getLevelName(level)
        extra['level'] = level_name

        # Add time to log
        time = datetime.utcnow()
        extra['time'] = time

        # Add level in message
        message = '{} [{}] {}'.format(level_name, time, message)

        self.logger.log(level, message, exc_info=exc_info, extra=extra)

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


# Deprecated - use more specific methods
def log_for_user(message, user_id, forward=False):
    message = "User: {} | {}".format(user_id, message)
    LOGGER.log(message, logging.INFO, extra={'user_id': user_id})
