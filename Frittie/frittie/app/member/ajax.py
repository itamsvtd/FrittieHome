from dajax.core import Dajax
from django.http import HttpResponseRedirect
from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
from frittie.helper.common_helper import get_member_login_object, get_JSON_exclude_fields, get_stream_content, get_duplicate_object
from frittie.app.main.models import Location, Notify, Member, Message
from frittie.helper.settings_helper import MEMBER_USER_RELATIONS
from friends.models import FriendshipRequest, Friendship
from django.contrib.auth.models import User
from frittie.settings import conn
import datetime
import user_streams

# When user make an add friend request, create FriendshipRequest object and set accepted to False
# Create Friendship object of both user if they are not created, and send notify to the receiver user
# Status: COMPLETE
# Note:
#		_member_add_request is the current login user who click add button to this view user
#		_member_receive_request is the current view user
@dajaxice_register
def add_friend(request,username):
	member_add_request = get_member_login_object(request)
	member_receive_request = Member.objects.get(user=User.objects.get(username=username))
	try:
		fr = FriendshipRequest.objects.get(from_user=member_add_request.user,to_user=member_receive_request.user,accepted=True)
		fr.accepted = False
		fr.save()
	except:
		FriendshipRequest.objects.create(from_user=member_add_request.user, to_user=member_receive_request.user, message='')
	try:
		Friendship.objects.get(user=member_add_request.user)
	except Friendship.DoesNotExist:
		Friendship.objects.create(user=member_add_request.user)
	try:
		Friendship.objects.get(user=member_receive_request.user)
	except Friendship.DoesNotExist:
		Friendship.objects.create(user=member_receive_request.user)
	if len(Notify.objects.filter(notify_type='add_friend',notify_to=member_receive_request,notify_from=member_add_request)) == 0:
		notify_type= 'add_friend'
		new_notify = Notify.objects.create(notify_type=notify_type,notify_to=member_receive_request,notify_from=member_add_request,status='new',date=datetime.datetime.now(),content='')
		content = ("<div class='notify-main-content'>" + 
						"<a href='/" + member_add_request.user.username + "/' >" + 
								member_add_request.user.first_name + " " + member_add_request.user.last_name + 
						"</a>" + 
							" want to be friend with you" + 
					"</div>" +
					"<div class='decide-btn-area'>" + 
						"<input type='hidden' id='get_username_notify" + str(new_notify.pk) + "' value='" + member_add_request.user.username + "' >" + 
						"<input type='button' class='btn btn-primary' value='Accept' onClick='handle_accept_friend_request(" + str(new_notify.pk) + ")'/>" + 
						"<input type='button' class='btn' value='Decline' onClick='handle_decline_friend_request(" + str(new_notify.pk) + ")' />" + 
					"</div>")
		new_notify.content = content
		new_notify.save()
		new_buzz_type = len(Notify.objects.filter(notify_to=member_receive_request,status='new'))
		new_mail_type = len(Message.objects.filter(member_receive=member_receive_request,status='new'))
		buzz = simplejson.dumps({'new_notify': new_mail_type+new_buzz_type,'new_buzz_type':new_buzz_type,'new_mail_type':new_mail_type, 'username': member_receive_request.user.username})
		conn.send(buzz,destination='/update')
	return simplejson.dumps({'username':username,'firstname': member_receive_request.user.first_name,'lastname': member_receive_request.user.last_name})

# Not notify user when they are unfriend
@dajaxice_register
def unfriend(request,username):
	member_login = get_member_login_object(request)
	member_view = Member.objects.get(user=User.objects.get(username=username))
	Friendship.objects.unfriend(member_login.user,member_view.user)
	return simplejson.dumps({'username':username,'firstname': member_view.user.first_name,'lastname': member_view.user.last_name, 'gender': member_view.gender, 'num_friends': len(member_view.get_friends()) })

@dajaxice_register
def accept_friend_request(request,username): 
	member_add_request = Member.objects.get(user=User.objects.get(username=username))
	member_receive_request = get_member_login_object(request)
	fr = FriendshipRequest.objects.filter(from_user=member_add_request.user, to_user=member_receive_request.user)
	print fr
	# In case member A click accept while the other member B already cancel the request
	# we handle by reload the page
	if len(fr) != 0:
		fr[0].accept()
		notify_type= 'accept_friend_request'
		content = ("<div class='notify-main-content'>" + 
						"<a href='/" + member_receive_request.user.username + "' >" + 
							member_receive_request.user.first_name + " " + member_receive_request.user.last_name + 
						"</a>" + 
						" accept your friend request" + 
					"</div>") 
		new_notify = Notify.objects.create(notify_type=notify_type,notify_to=member_add_request,notify_from=member_receive_request,status='new',date=datetime.datetime.now(),content=content)
		new_notify.save()
		n = Notify.objects.get(notify_type='add_friend',notify_to=member_receive_request,notify_from=member_add_request)
		new_content = ("<div class='notify-main-content'>" + 
							"<a href='/" + member_add_request.user.username + "' >" + 
								member_add_request.user.first_name + " " + member_add_request.user.last_name + 
							"</a>" + 
							" want to be friend with you" + 
						"</div>" +
						"<div class='notify-accept-friend-request'>" + 
							"You have accepted this request " + 
						"</div>")
		n.content = new_content
		n.notify_type = 'add_friend_response_accept'
		n.save()
		new_buzz_type = len(Notify.objects.filter(notify_to=member_add_request,status='new'))
		new_mail_type = len(Message.objects.filter(member_receive=member_add_request,status='new'))
		
		# Add and update streams
		friend_activity_content1 = get_stream_content('befriend','friends_content',{'member1':member_receive_request,'member2':member_add_request})
		user_activity_content1 = get_stream_content('befriend','user_content',{'member1':member_receive_request,'member2':member_add_request})
		list_friends_username1 = Friendship.objects.friends_of(member_receive_request.user).values_list('username', flat=True)
		friend_activity_content2 = get_stream_content('befriend','friends_content',{'member1':member_add_request,'member2':member_receive_request})
		user_activity_content2 = get_stream_content('befriend','user_content',{'member1':member_add_request,'member2':member_receive_request})
		list_friends_username2 = Friendship.objects.friends_of(member_add_request.user).values_list('username', flat=True)
		user_exclude = ''
		common_friend_username = get_duplicate_object(list(list_friends_username1)+list(list_friends_username2))
		if len(common_friend_username) > 0: 
			user_exclude=str(common_friend_username)
		user_streams.add_stream_item(member_receive_request.user, friend_activity_content1, user_activity_content1)
		user_streams.add_stream_item(member_add_request.user, friend_activity_content2, user_activity_content2, user_exclude)

		buzz = simplejson.dumps({'new_notify': new_buzz_type+new_mail_type,'new_buzz_type':new_buzz_type,'new_mail_type':new_mail_type, 'username': member_add_request.user.username, 'new_friend_activity1': friend_activity_content1, 'new_friend_activity2': friend_activity_content2, 'list_friends_username1': list(list_friends_username1), 'list_friends_username2': list(list_friends_username2) })
		conn.send(buzz,destination='/update')
		return simplejson.dumps({'username':username,'firstname': member_add_request.user.first_name,'lastname': member_add_request.user.last_name,'reload': "False"})
	else:
		return simplejson.dumps({'reload': "True"})

@dajaxice_register
def decline_friend_request(request,username):
	member_add_request = Member.objects.get(user=User.objects.get(username=username))
	member_receive_request = get_member_login_object(request)
	fr = FriendshipRequest.objects.filter(from_user=member_add_request.user, to_user=member_receive_request.user, accepted=False)
	if len(fr) != 0:
		fr[0].decline()
		n = Notify.objects.get(notify_type='add_friend',notify_to=member_receive_request,notify_from=member_add_request)
		new_content = ("<div class='notify-main-content'>" + 
							"<a href='/" + member_add_request.user.username + "' >" + 
								member_add_request.user.first_name + " " + member_add_request.user.last_name + 
							"</a>" + 
							" want to be friend with you" + 
						"</div>" + 
		 				"<div class='notify-decline-friend-request'>" +
		 					"You have declined this request" + 
		 				"</div>")
		n.content = new_content
		n.notify_type = 'add_friend_response_decline'
		n.save()
		return simplejson.dumps({'username':username,'firstname': member_add_request.user.first_name,'lastname': member_add_request.user.last_name,'reload':'False'})
	else:
		return simplejson.dumps({'reload':'True'})

@dajaxice_register
def cancel_friend_request(request,username):
	member_add_request = get_member_login_object(request)
	member_receive_request = Member.objects.get(user=User.objects.get(username=username))
	fr = FriendshipRequest.objects.filter(from_user=member_add_request.user, to_user=member_receive_request.user, accepted=False)
	if len(fr) != 0:
		fr[0].cancel()
		n = Notify.objects.get(notify_type='add_friend',notify_to=member_receive_request,notify_from=member_add_request)
		new_content = ("<div class='notify-main-content'>" + 
							"<a href='/" + member_add_request.user.username + "' >" + 
								member_add_request.user.first_name + " " + member_add_request.user.last_name + 
							"</a>" + 
							" want to be friend with you" + 
						"</div>" + 
						"<div class='notify-request-not-active'>" +
							" This request is no longer active " + 
						"</div>")
		n.content = new_content
		n.notify_type = 'friend_request_not_active'
		n.save()
		return simplejson.dumps({'username':username,'firstname': member_receive_request.user.first_name,'lastname': member_receive_request.user.last_name, 'reload': 'False', 'gender': member_receive_request.gender})
	else:
		return simplejson.dumps({'reload':'True'})

@dajaxice_register
def change_personal_public_status(request,username):
	return simplejson.dumps({'message':'Success'})

@dajaxice_register
def change_personal_private_status(request,username):
	return simplejson.dumps({'message':'Success'}) 

@dajaxice_register
def accept_activity_request(request,activity_id,member_join_id):
	return simplejson.dumps({'message':'Success'})

@dajaxice_register
def decline_activity_request(request,activity_id):
	return simplejson.dumps({'message':'Success'})

# Public activity allow everyone to see it
# Private activity just allow the host's friends to see it
@dajaxice_register
def change_activity_privacy_status(request,activity_id):
	return simplejson.dumps({'message':'Success'})

@dajaxice_register
def get_update_activity(request,username):
	return simplejson.dumps({'message':'Success'})

