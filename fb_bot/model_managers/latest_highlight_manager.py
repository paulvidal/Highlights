from fb_highlights.models import LatestHighlight


def get_all_highlights():
    return LatestHighlight.objects.all()


def already_has_highlight(link, time_since_added):
    return LatestHighlight.objects.filter(link=link, time_since_added=time_since_added)


def add_highlight(link, time_since_added):
    LatestHighlight.objects.create(link=link, time_since_added=time_since_added)


def delete_highlight(link, time_since_added):
    LatestHighlight.objects.filter(link=link, time_since_added=time_since_added).delete()