release: sh heroku_release.sh && python manage.py fix_db

web: gunicorn highlights.wsgi --workers 3
