from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('frittie.app.member.views',
	url(r"^$", "member_main_page"),
)
