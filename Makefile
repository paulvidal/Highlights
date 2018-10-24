SHELL := /bin/bash

run: prod
	sh runserver.sh

dev:
	cd static && yarn run server && cd ..

prod:
	cd static && yarn run prod && cd ..

clean:
	cd static && yarn run clean && cd ..

test:
	source set_env_var.sh && python manage.py test

explore:
	source set_env_var.sh && python manage.py test fb_highlights.tests.test_explore.ExploreTestCase.test_explore
