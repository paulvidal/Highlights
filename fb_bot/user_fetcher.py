import requests

from fb_bot.logger import logger
from fb_bot.messenger_manager import sender


def get_facebook_user_info(fb_id):
    response = requests.get("https://graph.facebook.com/{}/{}".format(sender.GRAPH_VERSION, fb_id),
                            params={"fields": "first_name, last_name, locale",
                                    "access_token": sender.ACCESS_TOKEN})

    if response.status_code != 200:
        logger.log_error_for_user("Could not retrieve facebook information", fb_id, extra={
            'fb_response': response.json()
        })
        return None

    json_response = response.json()

    facebook_id = fb_id
    first_name = json_response.get('first_name') if json_response.get('first_name') else 'default'
    last_name = json_response.get('last_name') if json_response.get('last_name') else 'default'
    locale = json_response.get('locale') if json_response.get('locale') else 'default'
    timezone = json_response.get('timezone') if json_response.get('timezone') else 0

    return facebook_id, first_name, last_name, locale, timezone


if __name__ == "__main__":
    fb_id = 1119096411506599
    print(get_facebook_user_info(fb_id))
