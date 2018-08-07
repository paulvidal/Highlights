# In order to make imports, set python path

import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Code

from apscheduler.schedulers.blocking import BlockingScheduler
from scheduler.utils import create_command
from highlights import settings

from rq import Queue
from scheduler import worker


scheduler = BlockingScheduler()
queue = Queue(connection=worker.CONNECTION)


@scheduler.scheduled_job('interval', minutes=4)
def broadcast_highlights():
    queue.enqueue(create_command('broadcast_highlights'))


@scheduler.scheduled_job('interval', minutes=2)
def add_video_info():
    queue.enqueue(create_command('add_video_info'))


@scheduler.scheduled_job('interval', minutes=10)
def check_highlight_validity():
    queue.enqueue(create_command('check_highlight_validity'))


"""
Fetch highlights
"""
@scheduler.scheduled_job('interval', minutes=5)
def fetch_highlights():
    queue.enqueue(create_command('fetch_highlight', arg='footyroom'))
    queue.enqueue(create_command('fetch_highlight', arg='ourmatch'))
    queue.enqueue(create_command('fetch_highlight', arg='sportyhl'))
    queue.enqueue(create_command('fetch_highlight', arg='highlightsfootball'))


@scheduler.scheduled_job('interval', minutes=60)
def fetch_highlights_hoofoot():
    if not settings.is_prod():
        queue.enqueue(create_command('fetch_highlight', arg='hoofoot'))


"""
Execute tasks before starting again
"""
fetch_highlights()
fetch_highlights_hoofoot()
broadcast_highlights()


scheduler.start()