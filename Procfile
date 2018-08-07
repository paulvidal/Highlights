release: python manage.py migrate

web: gunicorn highlights.wsgi --workers 3

clock: python scheduler/clock.py

worker: python scheduler/worker.py
