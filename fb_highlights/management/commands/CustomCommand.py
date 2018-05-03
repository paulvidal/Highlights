import abc

import time
from django.core.management import BaseCommand
from raven.contrib.django.raven_compat.models import client
from fb_bot.logger import logger
from highlights import settings


class CustomCommand(BaseCommand):

    def handle(self, *args, **options):
        try:
            start_time = time.time()
            self.run_task()
            # Monitor duration of the task
            logger.log("Task " + str(self.get_task_name()) + " executed in " + str(round(time.time() - start_time, 2)) + "s", forward=True)
        except Exception as error:
            if not settings.DEBUG:
                # Say if PROD or PRE-PROD
                client.user_context({ 'prod_status': settings.PROD_STATUS })
                # Report to sentry if problem detected
                client.captureException()
                # Report task had a problem
                logger.log("Task " + str(self.get_task_name()) + " failed", forward=True)
            else:
                raise error

    @abc.abstractmethod
    def get_task_name(self):
        """ Override method """

    @abc.abstractmethod
    def run_task(self):
        """ Override method """
