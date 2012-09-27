from django.conf.urls.defaults import *

urlpatterns = patterns('frittie.app.notify.views',
	url(r"^$", "show_notification"),
)

