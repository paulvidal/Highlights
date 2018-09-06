from fb_bot.messenger_manager import sender, formatter
from fb_bot.messages import *
from fb_bot.model_managers import user_manager
from fb_highlights.management.commands.CustomCommand import CustomCommand
from highlights import settings


class Command(CustomCommand):

    def get_task_name(self, options):
        return 'broadcast message'

    def run_task(self, options):
        all_ids = user_manager.get_all_users_id()

        text = "UEFA Nations League starts tonight! " + EMOJI_TROPHY + EMOJI_FIRE \
               + '\n\n' + "The newly created competition between european national teams will make its debut tonight!"\
               + '\n\n' + "SUBSCRIBE now to not miss a single match."

        messages = []

        # image asset id
        asset_id = 2183629061849013 if settings.is_prod() else 661776840874725

        messages.append(
            formatter.create_image_attachment_from_saved_asset(asset_id)
        )

        messages.append(
            formatter.create_quick_text_reply_message(
                text,
                [EMOJI_TROPHY + ' Add Nations League', EMOJI_CROSS + ' No thanks']
            )
        )

        sender.send_batch_multiple_facebook_messages(all_ids, messages)
