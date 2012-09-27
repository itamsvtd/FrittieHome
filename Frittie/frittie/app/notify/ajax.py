from dajax.core import Dajax
from django.http import HttpResponseRedirect
from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
from django.contrib.auth.models import User
from frittie.helper.common_helper import get_member_login_object, get_JSON_exclude_fields, get_stream_content, get_duplicate_object
from frittie.app.main.models import Location, Member, Notify, Message
from frittie.helper.settings_helper import MEMBER_USER_RELATIONS
from frittie.helper.common_helper import get_new_buzzes
from friends.models import FriendshipRequest, Friendship
from frittie.settings import conn, WEBSITE_HOMEPAGE
import datetime
import user_streams

@dajaxice_register
def delete_notification(request,notify_id):
	Notify.objects.get(pk=notify_id).delete()
	return simplejson.dumps({'notify_id': notify_id})

@dajaxice_register
def accept_friend_request(request,notify_id,username):
	member_add_request = Member.objects.get(user=User.objects.get(username=username))
	member_receive_request = get_member_login_object(request)
	new_content = ''
	fr = FriendshipRequest.objects.filter(from_user=member_add_request.user, to_user=member_receive_request.user)
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
		n = Notify.objects.get(pk=notify_id)
		new_content = ("<div class='notify-main-content'>" + 
							"<a href='/" + member_add_request.user.username + "' >" + 
								member_add_request.user.first_name + " " + member_add_request.user.last_name + 
							"</a>" + 
							" want to be friend with you" + 
						"</div>" +
						"<div class='notify-accept-friend-request'>" + 
							" You have accepted this request " + 
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
		return simplejson.dumps({'notify_id': str(notify_id), 'new_content': new_content, 'username':username,'firstname': member_add_request.user.first_name,'lastname': member_add_request.user.last_name,'reload': 'False'})
	else:
		return simplejson.dumps({'reload': 'True'})


@dajaxice_register
def decline_friend_request(request,notify_id,username):
	member_add_request = Member.objects.get(user=User.objects.get(username=username))
	member_receive_request = get_member_login_object(request)
	fr = FriendshipRequest.objects.filter(from_user=member_add_request.user, to_user=member_receive_request.user, accepted=False)
	if len(fr) != 0:		
		fr[0].decline()
		n = Notify.objects.get(pk=notify_id)
		new_content = ("<div class='notify-main-content'>" + 
							"<a href='/" + member_add_request.user.username + "' >" + 
								member_add_request.user.first_name + " " + member_add_request.user.last_name + 
							"</a>" + 
							" want to be friend with you" + 
						"</div>" +
						"<div class='notify-decline-friend-request'>" + 
							" You have declined this request " + 
						"</div>")
		n.content = new_content
		n.notify_type = 'add_friend_response_decline'
		n.save()
		return simplejson.dumps({'notify_id': str(notify_id), 'new_content': new_content, 'username':username,'firstname': member_add_request.user.first_name,'lastname': member_add_request.user.last_name,'reload': 'False'})
	else:
		return simplejson.dumps({'reload': 'True'})


