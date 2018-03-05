from fb_highlights.management.commands.CustomCommand import CustomCommand
from fb_bot import scheduler


class Command(CustomCommand):

    def get_task_name(self):
        return 'add video info'

    def run_task(self):
        scheduler.add_videos_info()