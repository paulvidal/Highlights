from fb_bot import scheduler_tasks
from fb_highlights.management.commands.CustomCommand import CustomCommand


class Command(CustomCommand):

    def add_arguments(self, parser):
        parser.add_argument('site_to_fetch')

    def get_task_name(self, options):
        return 'fetch highlight ' + options['site_to_fetch']

    def run_task(self, options):
        site = options['site_to_fetch']
        scheduler_tasks.fetch_highlights(site)