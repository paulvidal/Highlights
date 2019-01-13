from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management import call_command

from fb_highlights.management.commands.CustomCommand import CustomCommand


scheduler = BlockingScheduler()


@scheduler.scheduled_job('interval', minutes=2, seconds=30, max_instances=1)
def timed_job():
    call_command('broadcast_highlights')


@scheduler.scheduled_job('interval', minutes=2, seconds=30, max_instances=1)
def timed_job():
    call_command('add_video_info')


@scheduler.scheduled_job('interval', minutes=10, max_instances=1)
def timed_job():
    call_command('check_recent_highlights_validity')


@scheduler.scheduled_job('interval', hours=1, max_instances=1)
def timed_job():
    call_command('check_highlights_validity')


# Highlights fetching tasks

@scheduler.scheduled_job('interval', minutes=5, max_instances=3)
def timed_job():
    call_command('fetch_highlight', 'footyroom')


@scheduler.scheduled_job('interval', minutes=5, max_instances=3)
def timed_job():
    call_command('fetch_highlight', 'ourmatch')


@scheduler.scheduled_job('interval', minutes=5, max_instances=3)
def timed_job():
    call_command('fetch_highlight', 'sportyhl')


@scheduler.scheduled_job('interval', minutes=5, max_instances=3)
def timed_job():
    call_command('fetch_highlight', 'highlightsfootball')


@scheduler.scheduled_job('interval', minutes=30, max_instances=3)
def timed_job():
    call_command('fetch_highlight', 'hoofoot')


class Command(CustomCommand):

    def get_task_name(self, options):
        return 'Scheduler'

    def run_task(self, options):
        scheduler.start()