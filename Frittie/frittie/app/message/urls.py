from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('frittie.app.message.views',
	url(r"^$", "message_main_view"),
	url(r'^(?P<username>\w+)/','member_message'),
)
