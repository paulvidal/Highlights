release: python manage.py migrate fb_highlights 0029_auto_20180402_1904 && python manage.py add_competitions

web: gunicorn highlights.wsgi --workers 3
