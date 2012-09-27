from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.core import serializers
from settings_helper import USER_COMMON_INCLUDE_FIELDS, SESSION_KEY
from frittie.app.main.models import Member, Notify, Location
from frittie.helper.common_helper import convert_queryset_to_list
from django.utils import simplejson

# Check if this location is created by this current login user
def check_user_location(request, location_id):
	try:
		member = None
		if SESSION_KEY in request.session:
			member = Member.objects.get(user=User.objects.get(pk=request.session[SESSION_KEY]))
		location = Location.objects.get(pk=location_id,create_by=member)
	except Location.DoesNotExist:
		return False
	return True

# Check if this location is followed by this current login user
def check_user_follow(request,location_id):
	if SESSION_KEY in request.session:
		current_member = Member.objects.get(user=User.objects.get(pk=request.session[SESSION_KEY]))
		member_follow = Location.objects.get(pk=location_id).follow_by.all()
		for member in member_follow:
			if member.user.username == current_member.user.username:
				return True
	return False
		