from fb_bot.logger import logger
from fb_highlights.models import NewFootballRegistration


def add_football_registration(name, source, user=None):
    try:
        NewFootballRegistration.objects.update_or_create(name=name,
                                                         source=source,
                                                         user=user)
    except:
        # TODO: update this with a proper create without private key and tolerating duplicates
        logger.error("Failed to add new football registration")