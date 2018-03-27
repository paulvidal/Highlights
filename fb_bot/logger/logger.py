from logentries import LogentriesHandler
import logging

from highlights import settings


class LoggerWrapper:
    def __init__(self):
        self.logger = logging.getLogger('logentries')
        self.logger.setLevel(logging.INFO)

        logentries_token = settings.get_env_var("LOGENTRIES_TOKEN")
        self.logger.addHandler(LogentriesHandler(logentries_token))

        self.enabled = True

    def log(self, message, forward):
        if not self.enabled:
            return

        print(message)

        if forward and settings.is_prod():
            # Only send in production mode
            self.logger.info(log)

    def is_enabled(self):
        return self.enabled

    def disable(self):
        self.enabled = False


LOGGER = LoggerWrapper()


def disable():
    LOGGER.disable()


def log(message, forward=False):
    LOGGER.log(message, forward)


def log_for_user(message, user_id, forward=False):
    message = "User: {} | {}".format(user_id, message)
    LOGGER.log(message, forward)
