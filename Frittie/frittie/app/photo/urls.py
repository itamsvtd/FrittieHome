from django.conf.urls.defaults import *
from django.conf import settings

try:
    delete_url = settings.MULTI_FILE_DELETE_URL
except AttributeError:
    delete_url = 'multi_delete'

try:
    image_url = settings.MULTI_IMAGE_URL
except AttributeError:
    image_url = 'multi_image'

urlpatterns = patterns('frittie.app.photo.views',
    url(r'^'+delete_url+'/(\d+)/$', 'photo_delete'),
    url(r'^upload/$', 'photo_upload', name='upload'),
    url(r"^(?P<photo_type>\w+)/(?P<object_id>\d+)/(?P<photo_id>\d+)/$","show_photo"),
)