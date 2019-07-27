# API reference: https://cloudinary.com/documentation/image_upload_api_reference

import cloudinary.uploader
import cloudinary.api

from highlights import settings
from highlights.settings import PROD_STATUS

CLOUD_NAME = 'highlightsbot'
API_KEY = '618388125585167'
API_SECRET = settings.get_env_var('CLOUDINARY_SECRET')

TIMEOUT = 5  # 5s

def upload_image(url, public_id=None, overwrite=False):
    options = {
        'folder': '{}/highlights'.format(PROD_STATUS),
        'use_filename': False,
        'access_mode': 'public',
        'async': False,
        'overwrite': overwrite,
        'api_key': API_KEY,
        'api_secret': API_SECRET,
        'cloud_name': 'highlightsbot'
    }

    if public_id:
        options['public_id'] = str(public_id)

    result = cloudinary.uploader.upload(url, timeout=TIMEOUT, **options)
    url = result['url']  # Url of the created resource

    return url
