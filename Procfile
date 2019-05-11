release: sh heroku_release.sh

web: ddtrace-run gunicorn highlights.wsgi --workers 3 --name=highlightsbot
