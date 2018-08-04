SHELL := /bin/bash

run:
	sh runserver.sh

test:
	source set_env_var.sh && python manage.py test
