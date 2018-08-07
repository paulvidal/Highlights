from fb_bot import scheduler_tasks
from fb_highlights.management.commands.CustomCommand import CustomCommand


class Command(CustomCommand):

    def get_task_name(self, options):
        return 'convert videos'

    def run_task(self, options):
        scheduler_tasks.create_streamable_videos()
        scheduler_tasks.check_streamable_videos_ready()