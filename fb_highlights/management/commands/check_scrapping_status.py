from fb_bot import scheduler
from fb_highlights.management.commands.CustomCommand import CustomCommand


class Command(CustomCommand):

    def get_task_name(self):
        return 'check scrapping status'

    def run_task(self):
        scheduler.check_scrapping_status()