from logentries import LogentriesHandler
import logging

from highlights import settings

LOGGER = logging.getLogger('logentries')
LOGGER.setLevel(logging.INFO)

logentries_token = settings.get_env_var("LOGENTRIES_TOKEN")
LOGGER.addHandler(LogentriesHandler(logentries_token))


def log(message):
    print(message)
    _send_to_logentries(message)


def log_for_user(message, user_id):
    message = "User: " + str(user_id) + " | " + message
    print(message)
    _send_to_logentries(message)


def _send_to_logentries(log):
    if settings.is_prod():
        # Only send in production mode
        LOGGER.info(log)