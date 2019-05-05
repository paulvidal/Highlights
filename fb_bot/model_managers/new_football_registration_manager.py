from fb_highlights.models import NewFootballRegistration


def add_football_registration(name, source, user=None):
    NewFootballRegistration.objects.update_or_create(name=name,
                                                     source=source,
                                                     user=user)