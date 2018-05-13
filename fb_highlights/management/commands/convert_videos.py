from fb_bot import scheduler
from fb_highlights.management.commands.CustomCommand import CustomCommand


class Command(CustomCommand):

    def get_task_name(self):
        return 'convert videos'

    def run_task(self):
        scheduler.create_streamable_videos()
        scheduler.check_streamable_videos_ready()