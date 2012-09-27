####################################
#	Author: Dang Nguyen			   #
#	File: common_helper			   #
#   								   #
####################################

# Some common function used for any kind of app
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.db.models import Q
from django.core import serializers
from settings_helper import USER_COMMON_INCLUDE_FIELDS, SESSION_KEY
from frittie.app.main.models import Member, Notify, Location, Message, Activity
from django.utils import simplejson
from friends.models import UserBlocks
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
import collections
import datetime

def convert_ampm_to_24hr(hour,ampm):
	result = 0
  	if ampm == 'am':
  		if hour == 12: 
  			result = 0
  		else: 
  			result = hour
 	if ampm == 'pm':
 		if hour == 12: 
 			result = 12
 		else: 
 			result = 12 + hour
   	return result
  
  
def convert_time(date,time,ampm=None,date_separator='/',time_separator=':',format='mm/dd/yyyy'):
   	date_list = date.split(date_separator)
   	format_list = format.split('/')
   	year = int(date_list[2])
   	month = int(date_list[0])
   	day = int(date_list[1])
   	time_list = time.split(time_separator)
  	minute = int(time_list[1])
   	hour = 0
   	if ampm:
   		hour = convert_ampm_to_24hr(int(time_list[0]),ampm)
   	else:
   		hour = int(time_list[0])
   	new_time = datetime.datetime(year,month,day,hour,minute)
   	return new_time

def get_duplicate_object(l):
	l2 = collections.Counter(l)
	return [i for i in l2 if l2[i]>1]

def remove_duplicate_object(l):
	return list(set(l))

def set_fixed_string(s,s_len):
	if s_len >= len(s): 
		return s
	return s[:s_len] + '...'

# Convert queryset type to list. Note: cannot convert object
def convert_queryset_to_list(obj_queryset):
	result = []
	if len(obj_queryset) != 0:
		for obj in obj_queryset:
			result.append(obj)
	return result

# Return name like: Dang Nguyen to Dang-Nguyen
def get_value_from_name(name):
	return name.replace(" ","-").lower() 

# Return JSON of data with all fields in the parameter excluded
def get_JSON_exclude_fields(data,fields,extras_param,relations_param,convert=True):
	obj_list = convert_queryset_to_list(data)
	if len(obj_list) != 0:
		return serializers.serialize("json",data,indent=4,excludes=fields,extras=extras_param,relations=relations_param)
	else:
		return []

# Return JSON of data with all fields in the parameter included
def get_JSON_include_fields(data,fields,extras_param,relations_param,convert=True):
	obj_list = convert_queryset_to_list(data)
	if len(obj_list) != 0:
		return serializers.serialize("json",data,indent=4,fields=fields,extras=extras_param,relations=relations_param)
	else:
		return []

# Get current login user in JSON data format
def get_user_login_data(request):
	if SESSION_KEY in request.session:
		user_id = request.session[SESSION_KEY]
		fields = USER_COMMON_INCLUDE_FIELDS
		user = get_JSON_include_fields(User.objects.filter(pk=user_id),fields,[],[])
		return user
	else:
		return []

# Get current login user object
def get_user_login_object(request):
	if SESSION_KEY in request.session:
		user_id = request.session[SESSION_KEY]
		user = User.objects.filter(pk=user_id)
		if len(user) == 1:
			return user[0]
	return None

# Get the extended class of user (member class) object -> Use this one
def get_member_login_object(request):
	user_login = get_user_login_object(request)
	member_login = None
	if user_login != None:
		member_login = Member.objects.filter(user=user_login)[0]
	return member_login

# Get the new notification -> not test yet
def get_new_buzzes(request):
	if SESSION_KEY in request.session:
		user = User.objects.get(pk=request.session[SESSION_KEY])
		member = Member.objects.get(user=user)
		notifies = Notify.objects.filter(status="new",notify_to=member)
		return notifies
	return []

def get_new_mail(request):
	if SESSION_KEY in request.session:
		user = User.objects.get(pk=request.session[SESSION_KEY])
		member = Member.objects.get(user=user)
		mail = Message.objects.filter(status="new",member_receive=member)
		return mail
	return []
# Get the current ip from client to see their zip code and
# return appropriate location. Currently, this is not work with localhost
def get_ip_method1(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Version 2 of get IP function
def get_ip_method2(request):
    """Returns the IP of the request, accounting for the possibility of being
    behind a proxy.
    """
    ip = request.META.get("HTTP_X_FORWARDED_FOR", None)
    if ip:
        # X_FORWARDED_FOR returns client1, proxy1, proxy2,...
        ip = ip.split(", ")[0]
    else:
        ip = request.META.get("REMOTE_ADDR", "")
    return ip

# Setup the constant month tuple using for the form
def setup_constant_month():
	month_value = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
	l = []
	for i in range(1,13):
		l.append([i,month_value[i-1]])
	return tuple(tuple(x) for x in l)

# Like the above function but for day
def setup_constant_day():
	l = []
	for i in range(1,32):
		l.append([i,i])
	return tuple(tuple(x) for x in l)

# LIke the above function but for year
def setup_constant_year():
	l = []
	for i in range(1900,2012):
		l.append([i,i])
	return tuple(tuple(x) for x in l)

def get_location_autocomplete_data():
	locations = Location.objects.all()
	result = []
	for location in locations:
		result.append({ 
						'name': location.name, 
						'icon': location.avatar.url, 
					  	'description': location.category, 
					  	'value': 'location_'+str(location.pk),
					  	#'value': get_value_from_name(location.name),
					  	'type': 'location'
					  }
					 )
	return result
	#return simplejson.dumps(result,indent=2)

def get_activity_autocomplete_data(request):
	member_login = get_member_login_object(request)
	activities = remove_duplicate_object(Activity.objects.filter(Q(member_create=member_login) | Q(member_join=member_login)))
	result = []
	for activity in activities:
		print activity.id
		result.append({ 
						'name': activity.name, 
						'icon': activity.logo.url, 
					  	'description': set_fixed_string(activity.description,20), 
					  	'value':'activity_'+str(activity.pk),
					  	#'value': get_value_from_name(activity.name),
					  	'type': 'activity'
					  }
					 )
	return result
	#return simplejson.dumps(result,indent=2)


def get_friends_autocomplete_data(request,message=False):
	member_login = get_member_login_object(request)
	if member_login == None: return []
	friends = member_login.get_friends()
	result = []
	for friend in friends:
		conversation = Message.objects.filter(Q(member_send=member_login,member_receive=friend) | Q(member_send=friend,member_receive=member_login)).order_by('-date')
		last_chat = ""
		#print len(conversation)
		if len(conversation) != 0:
			#last_chat =  set_fixed_string(conversation[0].content_html,20)
			if conversation[0].member_send == member_login:
				last_chat = "<i class='icon-share-alt'></i>" + set_fixed_string(conversation[0].content,20)
			else:
				last_chat = set_fixed_string(conversation[0].content,20)				
		#print last_chat
		description = ""
		if message:
			description = last_chat
		result.append({
				'name': str(friend.user.first_name + " " + friend.user.last_name),
				'icon': friend.avatar.url,
				'description': str(description),
				'value': str(friend.user.username), 
				'type': 'member'
			})
	return result
	#return simplejson.dumps(result,indent=2)

def get_autocomplete_data(request):
	return simplejson.dumps(get_location_autocomplete_data() + get_activity_autocomplete_data(request) + get_friends_autocomplete_data(request),indent=2)

# Get category icon using in the index page
def get_category_icon():
	categories = CategoryIcon.objects.all()
	result = []
	for category in categories:
		result.append( { 'name': category.name, 'icon': category.icon, 'description': category.description})
	return simplejson.dumps(result,indent=2)

def check_user_block(user1,user2):
	if UserBlocks.objects.get(user=user1).is_block(user2) or UserBlocks.objects.get(user=user2).is_block(user1):
		return True
	else:
		return False

def get_mail_content(mail_type,context_data):
	template_name = 'text/email/' + mail_type + ".html"
	return render_to_string(template_name,context_data)

def get_stream_content(stream_type,content_type,context_data):
	template_name = 'text/streams/' + content_type + "/" + stream_type + '.txt'
	return render_to_string(template_name,context_data)

def send_email(mail_type,context_data,sender_email,recipient_email):
	return None