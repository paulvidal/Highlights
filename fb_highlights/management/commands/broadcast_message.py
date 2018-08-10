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

        text = EMOJI_FIRE + " FOOTBALL IS BACK " + EMOJI_FIRE \
               + '\n\n' + "Thanks god! After a wild world cup " + EMOJI_TROPHY + ", Premier league and Ligue 1 START AGAIN tonight!" \
               + '\n\n' + EMOJI_FOOTBALL + " Manchester United - Leicester" \
               + '\n'   + EMOJI_FOOTBALL + " Marseille - Toulouse" \
               + '\n\n' + "Do not forget to subscribe to your favourite teams to get the highlights!"

        messages = []

        # # image asset id
        # asset_id = 224641178132304 if settings.is_prod() else 1967392230174065
        #
        # messages.append(
        #     messenger_manager.create_image_attachment_from_saved_asset(asset_id)
        # )

        messages.append(
            messenger_manager.create_quick_text_reply_message(
                text,
                [EMOJI_ADD + ' Subscribe', EMOJI_ADD + ' Add Premier League', EMOJI_ADD + ' Add Ligue 1 ', EMOJI_CROSS + ' No thanks']
            )
        )

        messenger_manager.send_batch_multiple_facebook_messages(all_ids, messages)
