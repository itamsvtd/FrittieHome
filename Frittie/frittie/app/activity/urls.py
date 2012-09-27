from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('frittie.app.activity.views',
   url(r"^(?P<activity_id>\d+)/$","show_activity"),

)


