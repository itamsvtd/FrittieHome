from frittie.app.main.models import Activity, Location, ActivityRequest, Member
from django.contrib.auth.models import User
from django.utils import simplejson
from django.utils.timezone import localtime
from django.core import serializers
from django.db.models import Q
from frittie.helper.common_helper import get_JSON_exclude_fields, get_member_login_object
from frittie.helper.settings_helper import ACTIVITY_TODAY_FEEDS_RELATIONS, SESSION_KEY
from friends.models import Friendship
import datetime

# Check is current login user is the creator of this activity or not
def check_user_activity_create(request,activity_id):
	try:
		member = None
		if SESSION_KEY in request.session:
			member = Member.objects.get(user=User.objects.get(pk=request.session[SESSION_KEY]))
		activity = Activity.objects.get(pk=activity_id,member_create=member)
	except Activity.DoesNotExist:
		return False
	return True

# Check if current login user have joined this activity or not
def check_user_activity_join(request,activity_id):
	if SESSION_KEY in request.session:
		current_member = Member.objects.get(user=User.objects.get(pk=request.session[SESSION_KEY]))
		member_join = Activity.objects.get(pk=activity_id).member_join.all()
		for member in member_join:
			if member.user.username == current_member.user.username:
				return True
	return False

# Check if this activity can be seen by the current login user 
# -> If public, available to everyone. If private, only available to creator's friend
def check_activity_seeable(request,activity_id):
	activity = Activity.objects.get(pk=activity_id)
	if activity.activity_type != "invite_only": 
		return True
	else:
		#if SESSION_KEY in request.session:
		#	member_login = Member.objects.get(user=User.objects.get(pk=request.session[SESSION_KEY]))
		member_login = get_member_login_object(request)
		member_create = activity.member_create
		if member_login == member_create or member_login in activity.member_invite.all():
			return True
		return False
		#return False

def get_activity_unjoinable(request,activity_id):
	activity = Activity.objects.get(pk=activity_id)
	member_login = get_member_login_object(request)
	if len(activity.member_join.all()) == activity.limit:
		return "There is no more available spot for this activity "
	if activity.activity_type == 'blind_date':
		if member_login.gender == activity.member_create.gender:
			return "You are not qualified to join this activity. You and the host need to have different sex in the blind date activity"
	return None


# Check if this activity is today activity
def is_today_activity(activity_id):
	now = datetime.datetime.now()
	activity = Activity.objects.filter(pk=activity_id,start_time__year=now.year,start_time__month=now.month,start_time__day=now.day)
	if len(activity) != 0:
		return True
	return False

# Check if this activity is upcomming
def is_upcoming_activity(activity_id):
	now = datetime.datetime.now()
	if len(Activity.objects.filter(pk=activity_id,start_time__gt=now)) != 0:
		return True
	return False

# Check if this activity is already past
def is_past_activity(activity_id):
	now = datetime.datetime.now()
	if len(Activity.objects.filter(pk=activity_id,end_time__lt=now)) != 0:
		return True 
	return False

# Check if this activity is happening
def is_happening_activity(activity_id):
	now = datetime.datetime.now()
	if len(Activity.objects.filter(pk=activity_id,start_time__lte=now,end_time__gte=now)) != 0:
		return True
	return False

# Get all activity happen today
def get_today_activity():
	now = datetime.datetime.now()
	return Activity.objects.filter(start_time__year=now.year,start_time__month=now.month,start_time__day=now.day).order_by('start_time')

# Get all upcoming activity
def get_upcoming_activity(location_id):
	location = Location.objects.get(pk=location_id)
	now = datetime.datetime.now()
	return Activity.objects.filter(location=location,start_time__gt=now).order_by('start_time')

# Get all past activity
def get_past_activity(location_id):
	location = Location.objects.get(pk=location_id)
	now = datetime.datetime.now()
	return Activity.objects.filter(location=location,end_time__lt=now).order_by('end_time') 

# Get all happening activity
def get_happening_activity(location_id):
	location = Location.objects.get(pk=location_id)
	now = datetime.datetime.now()
	return Activity.objects.filter(location=location,start_time__lte=now,end_time__gte=now).order_by('start_time')

# Get the relationship between the current login user and the activity
# Return none if there is no initial relationship between them
def get_user_activity_request(request,activity_id):
	activity = Activity.objects.get(pk=activity_id)
	member_login = get_member_login_object(request)
	activity_user_request = ActivityRequest.objects.filter(activity=activity,member_join=member_login,member_create=activity.member_create)
	if len(activity_user_request) != 0:
		return activity_user_request[0]
	return None	

# Check if the activity is upcoming, happening, or past and change its status appropriately
def update_activity_status(activity):
	if is_upcoming_activity(activity.pk):
		activity.activity_status = 'Upcomming'
	if is_happening_activity(activity.pk):
		activity.activity_status = 'Happening'
	if is_past_activity(activity.pk):
		activity.activity_status = 'Past'
	activity.save()

# Return friends of current login user who join in this activity
def get_friends_join_activity(friends,activity):
	result = []
	if activity.member_create in friends:
		result.append(activity.member_create)
	for friend in friends:
		if friend in activity.member_join.all():
			result.append(friend)
	return result

# Trending activity are activity which have a lot of people join in
def get_trending_activity():
	return Activity.objects.all().order_by('-member_join_amount')[:10]

# Hot activity are activities which have high number of comment
def get_hot_activity():
	return Activity.objects.all().order_by('-comment_amount')[:10]
