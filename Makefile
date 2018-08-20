SHELL := /bin/bash

run:
	sh runserver.sh

dev:
	cd static && yarn run server && cd ..

prod:
	cd static && yarn run prod && cd ..

clean:
	cd static && yarn run clean && cd ..

test:
	source set_env_var.sh && python manage.py test