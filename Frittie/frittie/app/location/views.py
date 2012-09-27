from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from frittie.app.main.models import Location, Photo, Comment, Member, Activity
from forms import LocationForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson
from django.core import serializers
from frittie.helper.member_helper import  check_friendship
from frittie.helper.common_helper import get_user_login_data, get_JSON_exclude_fields, get_new_buzzes, convert_time
from frittie.helper.common_helper import get_member_login_object, get_autocomplete_data, get_new_mail
from frittie.helper.activity_helper import get_today_activity, get_upcoming_activity
from frittie.helper.activity_helper import get_past_activity, get_happening_activity
from frittie.helper.location_helper import check_user_location, check_user_follow
from django.contrib.auth.decorators import login_required
from friends.models import Friendship

def show_location(request,location_id): 
    # Autocomplete Data
    autocomplete_data = get_autocomplete_data(request)

    member_login = get_member_login_object(request)
    if request.method == 'POST':
        # Handle multiple POST request. The one below is for create activity
        if 'activity_name' in request.POST:
            new_activity = Activity()
            try:
                new_activity.name = request.POST['activity_name']
                new_activity.description = request.POST['activity_description']
                starttime_tmp = request.POST['activity_starttime'].split()
                new_activity.start_time = convert_time(starttime_tmp[0],starttime_tmp[1],starttime_tmp[2])
                endtime_tmp = request.POST['activity_endtime'].split()
                new_activity.end_time = convert_time(endtime_tmp[0],endtime_tmp[1],endtime_tmp[2])
                new_activity.member_create = member_login
                new_activity.location = Location.objects.get(pk=int(request.POST['location']))
                new_activity.activity_type = request.POST['activity_type']

                if new_activity.activity_type == 'blind_date':
                    new_activity.limit = 1
                    new_activity.age_range_start = int(request.POST['activity_age_range_from'])
                    new_activity.age_range_end = int(request.POST['activity_age_range_to'])
                else:
                    if 'activity_unlimited' not in request.POST:
                        new_activity.limit = request.POST['activity_limit']
                new_activity.save()
            except:
                return render_to_response("activity_template/admin_page/create_error.html",
                                            {
                                                "member_login": member_login,
                                                "autocomplete_data": autocomplete_data,
                                                'location_id':location_id
                                            },
                                            context_instance = RequestContext(request))
            return HttpResponseRedirect("/activity/" + str(new_activity.pk) + "/manage/")

    # User login and his/her friends
    new_buzzes = get_new_buzzes(request)
    new_mail = get_new_mail(request)
    new_notify = len(new_buzzes) + len(new_mail)
    friends = None
    if member_login != None:
        friends = member_login.get_friends()

    # Location Data
    location = get_object_or_404(Location, pk=location_id)
    is_user_location = check_user_location(request,location_id)
    is_user_follow = check_user_follow(request,location_id)
    location_photo = Photo.objects.filter(photo_type='location',object_id=location.pk)
    location_comment = Comment.objects.filter(comment_type='location',object_id=location.pk)
    for comment in location_comment:
        comment.save()
        
    # Activity for this location
    upcoming_activities = get_upcoming_activity(location_id)
    past_activities = get_past_activity(location_id)
    happening_activities = get_happening_activity(location_id)

    template = 'location_template/normal_page/main_page.html'
    if is_user_location:
        template = 'location_template/admin_page/main_page.html'

    return render_to_response(
            template,
            {
                "location": location,
                "member_login": member_login,
                'new_buzzes': new_buzzes,
                'new_mail': new_mail,
                'new_buzzes': new_buzzes,
                "friends": friends,
                #"is_user_location": is_user_location,
                "is_user_follow": is_user_follow,
                "location_photo": location_photo,
                "location_comment": location_comment,
                "autocomplete_data": autocomplete_data,
                'upcoming_activities': upcoming_activities,
                'past_activities': past_activities,
                'happening_activities': happening_activities,
            },
            context_instance = RequestContext(request)
        )

@login_required()
def create_location(request):
    member_login = get_member_login_object(request)
    if "error" in request.GET:
        return render_to_response(
                "location_template/page/create_error.html",
                {
                    "member_login": member_login,
                },
                context_instance=RequestContext(request)
            )
    if request.method=='POST':
        form = LocationForm(request.POST, request.FILES)
        if form.is_valid(): 
            try:
                name = request.POST['name']
                description = request.POST['description']
                category = request.POST['category']
                address1 = request.POST['address1']
                address2 = request.POST['address2']
                city = request.POST['city']
                state = request.POST['state']
                zip_code = request.POST['zip_code']
                new_location = Location.objects.create(
                                create_by=member_login,
                                name=name,
                                description=description,
                                address1=address1,
                                address2=address2,
                                city=city,
                                state=state,
                                zip_code=zip_code
                            )
                if "avatar" in request.FILES:
                    new_location.avatar = request.FILES['avatar']
                new_location.save() 
            except:
                return HttpResponseRedirect("/location/create/?error")
            return HttpResponseRedirect("/" + member_login.user.username + "?create=location")
    else:
        form = LocationForm()
    return render_to_response(
                "location_template/page/create.html", 
                {
                    "form": form,
                    'member_login': member_login,
                }, 
                context_instance=RequestContext(request))

@login_required()
def edit_location(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    member_login = get_member_login_object(request)
    if "error" in request.GET:
        return render_to_response(
                "location_template/page/edit_error.html",
                {
                    "member_login": member_login,
                },
                context_instance=RequestContext(request)
            )
    if request.method =='POST':
        form = LocationForm(request.POST)
        if form.is_valid(): 
            try:
                location.name = request.POST['name']
                location.description = request.POST['description']
                location.category = request.POST['category']
                location.address1 = request.POST['address1']
                location.address2 = request.POST['address2']
                location.city = request.POST['city']
                location.state = request.POST['state']
                location.zip_code = request.POST['zip_code']
                if "avatar" in request.FILES:
                    location.avatar = request.FILES['avatar']
                location.save() 
            except:
                return HttpResponseRedirect("/location/" + location_id + "/edit/?error")
            return HttpResponseRedirect("/" + member_login.user.username + "?edit=location")
    else:
        default_data = {
                "name": location.name, 
                "description": location.description,
                "category": location.category,
                "address1": location.address1,
                "address2": location.address2,
                "city": location.city,
                "state": location.state,
                "zip_code": location.zip_code,
                "avatar": location.avatar,
            }
        form = LocationForm(default_data)
    return render_to_response(
                    "location_template/page/edit.html", 
                    {
                        "form": form, 
                        "member_login": member_login,
                        "location":location,
                    }, 
                    context_instance=RequestContext(request))

@login_required()
def delete_location(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    try:
        location.activity_set.all().delete()
        location.delete()
        return HttpResponseRedirect("user/?act=delete&obj=location")
    except:
        return HttpResponseServerError("Delete error")
    
