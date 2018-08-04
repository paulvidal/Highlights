from fb_highlights.models import ScrappingStatus


def get_all_scrapping_status():
    return [(status.site_name.title(), status.ok) for status in ScrappingStatus.objects.all()]


def update_scrapping_status(site_name, ok):
    status, _ = ScrappingStatus.objects.get_or_create(site_name=site_name)
    status.ok = ok
    status.save()