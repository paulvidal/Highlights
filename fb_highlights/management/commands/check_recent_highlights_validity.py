from fb_bot import scheduler_tasks
from fb_highlights.management.commands.CustomCommand import CustomCommand


class Command(CustomCommand):

    def get_task_name(self, options):
        return 'check RECENT highlight availability'

    def run_task(self, options):
        scheduler_tasks.check_recent_highlight_validity()