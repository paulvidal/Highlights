import requests

from fb_bot import messenger_manager
from fb_bot.logger import logger


def get_facebook_user_info(fb_id):
    response = requests.get("https://graph.facebook.com/v2.6/" + str(fb_id),
                            params={"fields": "first_name, last_name, profile_pic, locale, timezone, gender",
                                    "access_token": messenger_manager.ACCESS_TOKEN})

    if response.status_code != 200:
        logger.log_for_user("Could not retrieve facebook information", fb_id)
        return None

    json_response = response.json()

    facebook_id = fb_id
    first_name = json_response.get('first_name') if json_response.get('first_name') else 'default'
    last_name = json_response.get('last_name') if json_response.get('last_name') else 'default'
    image_url = json_response.get('profile_pic') if json_response.get('profile_pic') else 'https://www.default-profile-pic.com'
    locale = json_response.get('locale') if json_response.get('locale') else 'default'
    timezone = json_response.get('timezone') if json_response.get('timezone') else 0
    gender = json_response.get('gender') if json_response.get('gender') else 'default'

    return facebook_id, first_name, last_name, image_url, locale, timezone, gender


if __name__ == "__main__":
    fb_id = 1119096411506599
    print(get_facebook_user_info(fb_id))
