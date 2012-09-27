from django.conf.urls import patterns, include, url
from frittie import settings
from django.conf import settings
from tastypie.api import Api
#from frittie.app.api.api import UserResource, MemberResource, LocationResource
#from frittie.app.api.api import ActivityTodayResource, ActivityResource, CommentResource
#from frittie.app.api.api import LocationResource
from allauth.account import views
from django.contrib import admin
from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()
admin.autodiscover()

frittie_api = Api(api_name='frittie')
#frittie_api.register(UserResource())
#frittie_api.register(MemberResource())
#frittie_api.register(LocationResource())
#frittie_api.register(ActivityResource())
#frittie_api.register(ActivityTodayResource())
#frittie_api.register(CommentResource())

urlpatterns = patterns('',
    # Admin URL
    url(r'^admin/', include(admin.site.urls)),

    # Allauth app URL
    url(r"^signup/$", views.signup, name="account_signup"),
    url(r"^login/$", views.login, name="account_login"),
    url(r"^password/change/$", views.password_change, name="account_change_password"),
    url(r"^password/set/$", views.password_set, name="account_set_password"),
    url(r"^logout/$", views.logout, name="account_logout"),
    url(r"^password/reset/$", views.password_reset, name="account_reset_password"),
    url(r"^password/reset/done/$", views.password_reset_done, name="account_reset_password_done"),
    url(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$", views.password_reset_from_key, name="account_reset_password_from_key"),

    # Haystack app URL
    url(r"^search/", include('haystack.urls')),

    # Django Facebook URL
    url(r"^facebook/",include('django_facebook.urls')),

    # Frittie URL
    url(r'^$', include('frittie.app.main.urls')),
    url(r'^settings/$','frittie.app.member.views.settings'),
    url(r'^error/$','frittie.app.main.views.show_error'),
    url(r'^buzz/$',include('frittie.app.notify.urls')),
    url(r'^messages/',include('frittie.app.message.urls')),
    url(r'^location/',include('frittie.app.location.urls')),
    url(r'^activity/',include('frittie.app.activity.urls')),
    url(r'^info/',include('frittie.app.info.urls')),
    url(r'^feeds/',include('frittie.app.feed.urls')),
    url(r'^friends/',include('frittie.app.friend.urls')),
    url(r'^photo/',include('frittie.app.photo.urls')),

    # API URL
    url(r'^api/', include(frittie_api.urls)),

    # Dajaxice URL
    url(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),

    # Media URL
    url(r'^asset/media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),

    url(r'^(?P<username>\w+)/',include('frittie.app.member.urls')),
)

