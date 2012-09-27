from django.conf.urls.defaults import *
from frittie import settings

urlpatterns = patterns('frittie.app.friend.views',
    url(r"^find/$", "find_friend"),
)
