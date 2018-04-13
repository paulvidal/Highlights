from fb_highlights.models import NewFootballCompetition


def add_football_competition(name, source):
    NewFootballCompetition.objects.update_or_create(name=name, source=source)