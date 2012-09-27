from django.conf.urls.defaults import *
from frittie import settings

urlpatterns = patterns('frittie.app.main.views',
    url(r"^$", "main_page"),
)
