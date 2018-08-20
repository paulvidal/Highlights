#!/usr/bin/env bash

# Apply migrations
python manage.py migrate

# Run build commands for Webpack
make prod