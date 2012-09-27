from django.conf.urls.defaults import *

urlpatterns = patterns('frittie.app.location.views',
   url(r"^(?P<location_id>\d+)/$","show_location"),
   url(r"^create/$","create_location"),
   url(r"^(?P<location_id>\d+)/edit/$","edit_location"),
   url(r"^(?P<location_id>\d+)/delete$","delete_location"),
   #url(r"^follow/(?P<location_id>\d+)/(?P<user_id>\w+)/$","follow_location")
)

