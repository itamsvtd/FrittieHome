from django.shortcuts import get_object_or_404, render_to_response
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import RequestContext
from frittie.app.main.models import Photo
from django.core.files.uploadedfile import UploadedFile
from django.utils import simplejson
from sorl.thumbnail import get_thumbnail
from django.views.decorators.csrf import csrf_exempt
from frittie.helper.common_helper import get_member_login_object, get_autocomplete_data, get_new_buzzes, get_new_mail

import logging
log = logging

@csrf_exempt
def photo_delete(request, pk):
    if request.method == 'POST':
        image = get_object_or_404(Photo, pk=pk)
        image.delete()
        return HttpResponse(str(pk))
    else:
        return HttpResponseBadRequest('Only POST accepted')

@csrf_exempt
def photo_upload(request):
    if request.method == 'POST':
        if request.FILES == None:
            return HttpResponseBadRequest('Must have files attached!')

        #getting file data for farther manipulations
        file = request.FILES[u'files[]']
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size
        log.info ('Got file: "%s"' % str(filename))

        #writing file manually into model
        #because we don't need form of any type.
        member_login = get_member_login_object(request)
        image = Photo()
        image.filename=str(filename)
        image.image=file
        image.key_data = image.key_generate
        image.member_post = member_login
        image.photo_type = request.session['photo_type']
        image.object_id = request.session['object_id']
        image.save()
        log.info('File saving done')

        #getting thumbnail url using sorl-thumbnail
        im = get_thumbnail(image, "80x80", quality=50)
        thumb_url = im.url

        #settings imports
        try:
            file_delete_url = settings.MULTI_FILE_DELETE_URL+'/'
            file_url = settings.MULTI_IMAGE_URL+'/'+image.key_data+'/'
        except AttributeError:
            file_delete_url = 'multi_delete/'
            file_url = 'multi_image/'+image.key_data+'/'

        #generating json response array
        result = []
        result.append({"name":filename, 
                       "size":file_size, 
                       "url":file_url, 
                       "thumbnail_url":thumb_url,
                       "delete_url":file_delete_url+str(image.pk)+'/', 
                       "delete_type":"POST",})
        response_data = simplejson.dumps(result)
        
        #checking for json data type
        #big thanks to Guy Shapiro
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
        else:
            mimetype = 'text/plain'
        return HttpResponse(response_data, mimetype=mimetype)
    else: #GET
        return HttpResponse('Only POST accepted')

def show_photo(request,photo_type,object_id,photo_id):
    all_photo = Photo.objects.filter(photo_type=photo_type,object_id=object_id)
    current_photo = get_object_or_404(Photo,pk=photo_id)
    member_login= get_member_login_object(request)
    autocomplete_data = get_autocomplete_data(request)
    new_buzzes = get_new_buzzes(request)
    new_mail = get_new_mail(request)
    new_notify = len(new_buzzes) + len(new_mail)
    return render_to_response('photo_template/page/main_page.html',
                                {
                                    'autocomplete_data': autocomplete_data,
                                    'member_login': member_login,
                                    'current_photo': current_photo,
                                    'all_photo': all_photo,
                                    'new_buzzes': new_buzzes,
                                    'new_mail': new_mail,
                                    'new_notify': new_notify
                                },
                                context_instance = RequestContext(request)
                            )

# def multi_show_uploaded(request, key):
#     """Simple file view helper.
#     Used to show uploaded file directly"""
#     image = get_object_or_404(Photo, key_data=key)
#     url = settings.MEDIA_URL+image.image.name
#     return render_to_response('photo_template/one_image.html', {"multi_single_url":url,})