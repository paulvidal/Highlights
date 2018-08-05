from fb_bot.messages import *
from fb_bot.model_managers import user_manager
from fb_bot.model_managers import registration_competition_manager
from fb_highlights.management.commands.CustomCommand import CustomCommand
from fb_bot import messenger_manager
from highlights import settings


class Command(CustomCommand):

    def get_task_name(self, options):
        return 'broadcast message'

    def run_task(self, options):
        all_ids = user_manager.get_all_users_id()

        ids_subscribed_to_world_cup = registration_competition_manager.get_users_for_competition('world cup')
        ids_not_subscribed_to_world_cup = [id for id in all_ids if id not in ids_subscribed_to_world_cup]

        text = EMOJI_FIRE + " WORLD CUP BEGINS TODAY! " + EMOJI_FIRE \
            + '\n\n' + "Subscribe to the competition to not miss a single match!"

        messages = []

        # image asset id
        asset_id = 224641178132304 if settings.is_prod() else 1967392230174065

        messages.append(
            messenger_manager.create_image_attachment_from_saved_asset(asset_id)
        )

        messages.append(
            messenger_manager.create_quick_text_reply_message(
                text,
                ['Subscribe ' + EMOJI_TROPHY, 'No thanks ' + EMOJI_CROSS]
            )
        )

        messenger_manager.send_batch_multiple_facebook_messages(ids_not_subscribed_to_world_cup, messages)