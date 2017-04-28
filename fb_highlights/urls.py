from django.conf.urls import include, url
from .views import HighlightsBotView


urlpatterns = [
    url(r'^d08fcf03937a116ab14ea30725c72d33ac715bcfa085e296cd/?$', HighlightsBotView.as_view())
]