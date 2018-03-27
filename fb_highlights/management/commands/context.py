from django.core.management import BaseCommand

from fb_bot.model_managers import user_manager, context_manager


class Command(BaseCommand):

    def handle(self, *args, **options):
        user_ids = user_manager.get_all_users_id()

        for id in user_ids:
            user = user_manager.get_user(id)

            if user.context == 0:
                context_manager.update_context(id, context_manager.ContextType.SEARCH_HIGHLIGHTS)