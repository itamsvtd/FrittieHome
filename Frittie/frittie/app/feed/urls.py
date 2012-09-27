from django.conf.urls.defaults import *
from frittie import settings

urlpatterns = patterns('frittie.app.feed.views',
    url(r"^$", "show_feeds"),
)
