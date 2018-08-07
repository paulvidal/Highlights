# In order to make imports, set python path

import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Set up DJANGO project

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'highlights.settings')
django.setup()

# Code

import redis
from rq import Worker, Queue, Connection
from highlights import settings

LISTEN = ['high', 'default', 'low']

REDIS_URL = settings.get_env_var('REDISTOGO_URL')

CONNECTION = redis.from_url(REDIS_URL)


if __name__ == '__main__':
    with Connection(CONNECTION):
        worker = Worker(map(Queue, LISTEN))
        worker.work()