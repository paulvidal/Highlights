from fb_highlights.management.commands.CustomCommand import CustomCommand
from fb_bot import scheduler


class Command(CustomCommand):

    def get_task_name(self, options):
        return 'check highlight availability'

    def run_task(self, options):
        scheduler.check_highlight_validity()