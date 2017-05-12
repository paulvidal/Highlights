#!/usr/bin/env bash

echo "Setting highlights environment"

source environment.sh

echo "-> Updating requirements.txt"

pip freeze > requirements.txt

echo "-> Pushing to git"

git push --force-with-lease