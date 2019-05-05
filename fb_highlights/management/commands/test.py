from fb_bot.model_managers import user_manager
from fb_bot.user_fetcher import get_facebook_user_info
from fb_highlights.management.commands.CustomCommand import CustomCommand
from fb_highlights.models import User


class Command(CustomCommand):

    def get_task_name(self, options):
        return 'test'

    def run_task(self, options):
        users = list(User.objects.filter(
            first_name='user',
            last_name='last',
        ))

        for u in users:
            infos = get_facebook_user_info(u.facebook_id)

            if infos is None:
                continue

            facebook_id, first_name, last_name, locale, timezone = infos

            u.first_name = first_name
            u.last_name = last_name
            u.locale = locale
            u.save()

            print(facebook_id)