from fb_bot.messages import *
from fb_bot.model_managers import user_manager
from fb_highlights.management.commands.CustomCommand import CustomCommand
from fb_bot import messenger_manager


class Command(CustomCommand):

    def get_task_name(self):
        return 'broadcast message'

    def run_task(self):
        all_ids = user_manager.get_all_users_id()

        text = EMOJI_FIRE + " Brand new feature " + EMOJI_FIRE \
            + '\n\n' + "You can now subscribe to competitions!" \
            + '\n\n' + "e.g. Champions League, Premier League, La Liga..."

        message = messenger_manager.create_quick_text_reply_message(
            text,
            ['Add competition ' + EMOJI_TROPHY, 'No thanks ' + EMOJI_CROSS],
        )

        messenger_manager.send_batch_facebook_message(all_ids, message)

