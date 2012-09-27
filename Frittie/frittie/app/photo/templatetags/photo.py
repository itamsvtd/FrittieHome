from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('photo_template/upload.html')
def multiupform():
    return {'static_url':settings.MEDIA_URL,}
