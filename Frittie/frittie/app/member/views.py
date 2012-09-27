# Views for the main app
from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from frittie.app.main.models import Member, Location, Activity, LocationCategory
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.db.models import Q
from django.utils import simplejson
from django.core import serializers
from frittie.helper.member_helper import  check_friendship, check_user_login_page, check_confirm_email, get_friend_activity_stream
from frittie.helper.common_helper import get_user_login_object, get_new_buzzes, get_autocomplete_data, get_new_mail, convert_time
from frittie.helper.common_helper import get_JSON_exclude_fields, get_member_login_object, check_user_block
from frittie.helper.activity_helper import get_today_activity
from frittie.helper.settings_helper import SESSION_KEY
from django.contrib.auth.decorators import login_required
from frittie.app.member.forms import SettingForm
from frittie.helper.member_helper import validate_email_setting, validate_username_setting
from frittie.settings import NORMAL_STREAM_LIMIT
import datetime
import user_streams


# Done
def member_main_page(request, username):
	autocomplete_data = get_autocomplete_data(request)

	request.session['current_user'] = username
	
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
                                                'location_id': int(request.POST['location'])
                                            },
                                            context_instance = RequestContext(request))
			return HttpResponseRedirect("/activity/" + str(new_activity.pk) + "/manage/")

		if 'location_name' in request.POST:
			new_location = Location()
			try:
				new_location.name = request.POST['location_name']
				new_location.description = request.POST['location_description']
				new_location.category = request.POST['location_category']
				new_location.address1 = request.POST['location_address1']
				new_location.address2 = request.POST['location_address2']
				new_location.city = request.POST['location_city']
				new_location.state = request.POST['location_state']
				new_location.zip_code = int(request.POST['location_zipcode'])
				new_location.preference = request.POST['location_preference']
				new_location.create_by = member_login
				if "location_avatar" in request.FILES:
					new_location.avatar = request.FILES['location_avatar']
				new_location.save()
			except:
				return render_to_response("location_template/page/create_error.html",
                                            {
                                               "member_login": member_login,
                                                "autocomplete_data": autocomplete_data,
                                            },
                                            context_instance = RequestContext(request))
			return HttpResponseRedirect("/location/" + str(new_location.pk))

	if member_login != None:
		if check_confirm_email(request) == False: 
			notice = "resend_email"

	member_view = get_object_or_404(Member,user=get_object_or_404(User,username=username))
	template = ""
	section = None
	notice = None
	if 'section' in request.GET:
		section = request.GET['section']
	else:
		section = 'activity'

	# Define whether this is user login page or not. If yes, return 
	# his/her admin page. If not return the view page of this user
	if check_user_login_page(request,username):
		if "act" in request.GET:
			notice = request.GET['act']
		template = "member_template/admin_page/main_page.html"
		is_friend = None
	else:
		if member_login != None:
			if check_user_block(member_login.user,member_view.user):
				raise Http404
		template = "member_template/normal_page/main_page.html"
		is_friend = check_friendship(request,username)

	# Necessary data here
	new_buzzes = get_new_buzzes(request)
	new_mail = get_new_mail(request)
	new_notify = len(new_buzzes) + len(new_mail)
	location_create = Location.objects.filter(create_by=member_view)
	location_follow = Location.objects.filter(follow_by=member_view)
	location_categories = LocationCategory.objects.all()
	activity_create = Activity.objects.filter(member_create=member_view)
	activity_join = Activity.objects.filter(member_join=member_view)
	friends = member_view.get_friends()
	recent_activity_stream = user_streams.get_stream_items(User.objects.get(username=username))[:NORMAL_STREAM_LIMIT]
	friends_activity_stream = get_friend_activity_stream(request,'friend_content')[:NORMAL_STREAM_LIMIT]
	
	# Return the response and render the template view
	return render_to_response(
			template,
			{
				'autocomplete_data': autocomplete_data,
				'is_friend': is_friend,
				"notice": notice,
				'section': section,
				"new_buzzes": new_buzzes,
				'new_mail': new_mail,
				'new_notify': new_notify,
				"member_login": member_login,
				'member_view': member_view,
				'location_create': location_create,
				'location_follow': location_follow,
				'location_categories': location_categories,
				'activity_create': activity_create,
				'activity_join': activity_join,
				'friends': friends,
				'recent_activity_stream': recent_activity_stream,
				'friends_activity_stream': friends_activity_stream,
			},
			context_instance=RequestContext(request)
		)

@login_required()
def settings(request):
	member_login = get_member_login_object(request)

	# If there are parameter f in setting url, this mean the edit
	# setting process got some error, render a setting error template
	if "error" in request.GET:
		return render_to_response(
				"member_template/admin_page/settings_error.html",
				{
					"member_login": member_login,
				},
				context_instance=RequestContext(request)
			)

	user = get_object_or_404(User, pk=request.session[SESSION_KEY])
	member = Member.objects.get(user=user)
	if request.method == 'POST': 
		form = SettingForm(request.POST,request.FILES) 
		if form.is_valid(): 
			# Check if the new username and email already
			# exist and raise the appropriate error message
			flag = False
			check_username = validate_username_setting(request)
			if check_username == -1:
				form._errors["username"] = ErrorList([u"Usernames can only contain letters, numbers and underscores."])
			elif check_username == 0:
				form._errors["username"] = ErrorList([u"This username is already taken. Please choose another."])
			else:
				flag = True
			if validate_email_setting(request) == -1:
				form._errors["email"] = ErrorList([u"A user is registered with this e-mail address."])
				flag = False
			if flag:
				try:
					# Save the new data to the object user and member (model Member)
   					user.username = request.POST['username']
					user.first_name = request.POST['first_name']
					user.last_name = request.POST['last_name']
					user.email = request.POST['email']
					member.basic_info = request.POST['basic_info']
					member.gender = request.POST['gender']
					day = int(request.POST['birthdate_day'])
					month = int(request.POST['birthdate_month'])
					year = int(request.POST['birthdate_year'])
					member.birthdate  = datetime.date(year,month,day)
					if "avatar" in request.FILES:
						member.avatar = request.FILES['avatar']
					member.city = request.POST['city']
					member.state = request.POST['state']
					user.save()
					member.save()
				except:
					# give the parameter error in the url link so the website
					# render the error in setting page
					return HttpResponseRedirect("/settings/?error")
				# redirect to user main page if the edit process is successful
				return HttpResponseRedirect("/" + user.username + "/?act=edit_profile")
	else:
		# The initial data of the form taken from the user database 
		default_data = {
		       	"username": user.username, 
		       	"first_name": user.first_name,
				"last_name": user.last_name,
		       	"email": user.email,
		       	"basic_info": member.basic_info,
		       	"avatar": member.avatar,
		       	"city": member.city,
		    	"state": member.state,
		   	}
		if member.birthdate != None:
			default_data["birthdate_day"] = member.birthdate.day
			default_data["birthdate_month"] = member.birthdate.month
			default_data["birthdate_year"] = member.birthdate.year
		form = SettingForm(default_data) 

	return render_to_response(
		"member_template/admin_page/settings.html",
		{
			"form":form,
			"username":user.username,
			"member_login":member_login,
		},
		context_instance=RequestContext(request)
	)
