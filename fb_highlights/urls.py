from django.conf.urls import url
from fb_highlights import views

urlpatterns = [
    url(r'^d08fcf03937a116ab14ea30725c72d33ac715bcfa085e296cd/?$', views.HighlightsBotView.as_view()),
    url(r'^highlights/?$', views.HighlightsView.as_view()),
    url(r'^highlight/?$', views.HighlightRedirectView.as_view()),
    url(r'^debug', views.DebugPageView.as_view()),
    url(r'^privacy', views.PrivacyPageView.as_view()),
    url(r'^analytics', views.Analytics.as_view()),
    url(r'^status', views.Status.as_view()),
    url(r'^', views.Index.as_view()),
]