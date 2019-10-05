import os

DEBUG = "TRUE" == os.environ.get('DEBUG_ENABLE', "TRUE")

# GET BASE URL OF SERVER
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:8000/')

# STATUS OF SERVER - either "test | staging | prod"
PROD_STATUS = os.environ.get('PROD_STATUS', 'test')
