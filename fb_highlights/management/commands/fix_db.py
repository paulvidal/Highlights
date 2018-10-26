from datetime import datetime

from django.db.models import Min

from fb_highlights.management.commands.CustomCommand import CustomCommand
from fb_highlights.models import LatestHighlight


class Command(CustomCommand):

    def get_task_name(self, options):
        return 'fix db'

    def run_task(self, options):
        highlights = LatestHighlight.objects \
            .values('team1', 'score1', 'team2', 'score2', 'category') \
            .annotate(time_since_added=Min('time_since_added')) \
            .order_by('time_since_added')

        i = 1

        for m in highlights:
            hs = LatestHighlight.objects.filter(team1=m['team1'], team2=m['team2'], category=m['category'], score1=m['score1'], score2=m['score2'])
            d = datetime.fromordinal(m['time_since_added'].date().toordinal())

            for h in hs:
                h.id = i
                h.match_time = d
                h.save()

            i += 1