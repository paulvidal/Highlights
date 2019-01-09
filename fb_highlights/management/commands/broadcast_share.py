from fb_bot.messages import *
from fb_bot.model_managers import user_manager
from fb_highlights.management.commands.CustomCommand import CustomCommand
from fb_bot.messenger_manager import formatter, sender
from highlights import settings


class Command(CustomCommand):

    def get_task_name(self, options):
        return 'broadcast message'

    def run_task(self, options):
        all_ids = user_manager.get_all_users_id()

        message = formatter.create_generic_attachment([
            {
                "title": "Don’t be selfish...",
                "subtitle": "Your friends also deserve to see the goals! " + EMOJI_WINK,
                "image_url": settings.STATIC_URL + "/img/share_world_cup_meme.png",
                "buttons": [
                    {
                        "type": "element_share",
                        "share_contents": formatter.create_generic_attachment([
                            {
                                "title": "Don't miss the World Cup!",
                                "subtitle": "I will send you World Cup highlight videos for your favourite teams ASAP",
                                "image_url": settings.STATIC_URL + "/img/logo_share.png",
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

        sender.send_batch_facebook_message(all_ids, message)