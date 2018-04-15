from fb_bot.model_managers import user_manager
from fb_highlights.management.commands.CustomCommand import CustomCommand
from fb_bot import messenger_manager

import emoji


class Command(CustomCommand):

    def get_task_name(self):
        return 'broadcast message'

    def run_task(self):
        all_ids = user_manager.get_all_users_id()

        text = "New feature available " + emoji.emojize(":loudspeaker:") \
            + '\n\n' + "You can now subscribe to competitions such as Premier League, La Liga or even Ligue 1"

        message = messenger_manager.create_quick_text_reply_with_payload_message(
            text,
            ['Add competition', "I'm good"],
            ['add_registration', 'no_action']
        )

        messenger_manager.send_batch_facebook_message(all_ids, [message] * len(all_ids))

