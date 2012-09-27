from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
from friends.models import FriendshipRequest, Friendship
from django.contrib.auth.models import User
from frittie.settings import conn
from frittie.helper.common_helper import get_stream_content, get_member_login_object
from frittie.app.main.models import Activity, Location, Photo
import user_streams

@dajaxice_register
def upload_activity_photo(request,activity_id):
	request.session['photo_type'] = 'activity'
	request.session['object_id'] = int(activity_id)
	request.session['num_photo'] = len(Photo.objects.filter(photo_type='activity',object_id=activity_id))
	return simplejson.dumps({})

@dajaxice_register
def upload_location_photo(request,location_id):
	request.session['photo_type'] = 'location'
	request.session['object_id'] = int(location_id)
	request.session['num_photo'] = len(Photo.objects.filter(photo_type='location',object_id=location_id))
	return simplejson.dumps({})

@dajaxice_register
def update_streams(request):
	if request.session['allow_upload_stream']:
		if len(Photo.objects.filter(photo_type=request.session['photo_type'],object_id=request.session['object_id'])) > int(request.session['num_photo']):
			member_login = get_member_login_object(request)
			friend_activity_content, user_activity_content = '',''
			if request.session['photo_type'] == 'activity':
				activity = Activity.objects.get(pk=request.session['object_id'])
				friend_activity_content = get_stream_content('upload_activity_photo','friends_content',{'member_login':member_login,'activity':activity})
				user_activity_content = get_stream_content('upload_activity_photo','user_content',{'member_login':member_login,'activity':activity})
			else:
				location = Location.objects.get(pk=request.session['object_id'])
				friend_activity_content = get_stream_content('upload_location_photo','friends_content',{'member_login':member_login,'location':location})
				user_activity_content = get_stream_content('upload_location_photo','user_content',{'member_login':member_login,'location':location})
			list_friends_username = Friendship.objects.friends_of(member_login.user).values_list('username', flat=True)
			user_streams.add_stream_item(member_login.user, friend_activity_content, user_activity_content)
			buzz = simplejson.dumps({'new_friend_activity': friend_activity_content, 'list_friends_username': list(list_friends_username) })
			conn.send(buzz,destination='/update')
			request.session['allow_upload_stream'] = False
	return simplejson.dumps({})

