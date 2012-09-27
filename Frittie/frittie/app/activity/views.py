# Create your views here.from frittie.main.views import *
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from frittie.app.main.models import Activity, Comment, Photo, Location
from django.contrib.auth.models import User
import datetime
from django.utils import simplejson
from django.core import serializers
from frittie.helper.common_helper import get_autocomplete_data, get_member_login_object, get_new_buzzes, get_new_mail
from frittie.helper.activity_helper import check_user_activity_create, get_user_activity_request, get_friends_join_activity
from frittie.helper.activity_helper import check_user_activity_join, check_activity_seeable, get_activity_unjoinable, update_activity_status
from django.contrib.auth.decorators import login_required

def show_activity(request,activity_id):
    request.session['allow_upload_stream'] = True

    # Autocomplete Data
    autocomplete_data = get_autocomplete_data(request)

    # Activity object
    activity = get_object_or_404(Activity, pk=activity_id)

    # Update activity status, activity comment amount, and activity member join amount
    activity.update_comment_amount()
    activity.update_member_amount()
    update_activity_status(activity)           

    # Activity data  
    activity_photo = Photo.objects.filter(photo_type='activity',object_id=activity.pk)
    activity_user_request = get_user_activity_request(request,activity_id)
    activity_location = activity.location 
    activity_location_photo = Photo.objects.filter(photo_type='location',object_id=activity_location.pk)
    activity_comment = Comment.objects.filter(comment_type='activity',object_id=activity.pk)
    activity_unjoinable = get_activity_unjoinable(request,activity_id) 
    for comment in activity_comment:
        comment.save()

    # User login and his/her friends
    member_login = get_member_login_object(request)
    new_buzzes = get_new_buzzes(request)
    new_mail = get_new_mail(request)
    new_notify = len(new_buzzes) + len(new_mail)
    friends = None
    friends_join = None
    if member_login != None:
        friends = member_login.get_friends()
        friends_join = get_friends_join_activity(friends,activity)

    # Boolean data to define the interaction of the page
    is_user_activity_create = check_user_activity_create(request,activity_id)
    is_user_activity_join = check_user_activity_join(request,activity_id)
    is_activity_seeable = check_activity_seeable(request,activity_id)

    # Return corresponding template based on the boolean data
    # If activity is public, everyone can see it. If it is private
    # only friend of the host can see it.
    template = "activity_template/normal_page/" + activity.activity_type + "_main_page.html"
    if is_activity_seeable == False:
        template = "activity_template/normal_page/authorize_activity_notice.html"    
    if is_user_activity_create:
        template = "activity_template/admin_page/main_page.html"

    return render_to_response(
                            template, 
                            {
                                'autocomplete_data': autocomplete_data,
                                'activity': activity, 
                                'activity_comment': activity_comment,
                                'activity_photo': activity_photo,
                                'activity_user_request':activity_user_request,
                                'activity_location': activity_location,
                                'activity_location_photo': activity_location_photo,
                                'activity_unjoinable': activity_unjoinable,
                                'is_user_activity_join': is_user_activity_join,
                                'friends': friends,
                                'friends_join': friends_join,
                                'member_login': member_login,
                                'new_buzzes': new_buzzes,
                                'new_mail': new_mail,
                                'new_notify': new_notify
                            },
                            context_instance = RequestContext(request))

