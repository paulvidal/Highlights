from fb_highlights.management.commands.CustomCommand import CustomCommand
from fb_bot import scheduler


class Command(CustomCommand):

    def get_task_name(self, options):
        return 'broadcast highlights'

    def run_task(self, options):
        scheduler.send_most_recent_highlights()