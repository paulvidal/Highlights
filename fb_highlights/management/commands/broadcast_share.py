from fb_bot.messages import *
from fb_bot.model_managers import user_manager
from fb_highlights.management.commands.CustomCommand import CustomCommand
from fb_bot import messenger_manager
from highlights import settings


class Command(CustomCommand):

    def get_task_name(self):
        return 'broadcast message'

    def run_task(self):
        all_ids = user_manager.get_all_users_id()

        message = messenger_manager.create_generic_attachment([
            {
                "title": "Don’t be selfish...",
                "subtitle": "Your friends also deserve to see the goals! " + EMOJI_WINK,
                "image_url": settings.BASE_URL + "/static/images/share_world_cup_meme.png",
                "buttons": [
                    {
                        "type": "element_share",
                        "share_contents": messenger_manager.create_generic_attachment([
                            {
                                "title": "Don't miss the World Cup!",
                                "subtitle": "I will send you World Cup highlight videos for your favourite teams ASAP",
                                "image_url": settings.BASE_URL + "/static/images/logo_share.png",
                                "default_action": {
                                    "type": "web_url",
                                    "url": "https://m.me/highlightsSportBot/"
                                },
                                "buttons": [
                                    {
                                        "type": "web_url",
                                        "url": "https://m.me/highlightsSportBot/",
                                        "title": "Start " + EMOJI_HEART
                                    }
                                ]
                            }
                        ])
                    }
                ]
            }
        ])

        messenger_manager.send_batch_facebook_message(all_ids, message)