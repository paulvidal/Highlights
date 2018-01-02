from fb_highlights.models import NewFootballTeam


def add_football_team(name, source):
    NewFootballTeam.objects.update_or_create(name=name, source=source)