release: python manage.py migrate && python manage.py change_football_team_names && python manage.py change_football_competition_names

web: gunicorn highlights.wsgi --workers 3
