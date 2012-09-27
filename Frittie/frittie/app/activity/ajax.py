from dajax.core import Dajax
from django.http import HttpResponseRedirect
from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
from frittie.helper.common_helper import get_member_login_object, get_user_login_object, get_JSON_exclude_fields, get_stream_content, set_fixed_string
from frittie.app.main.models import Notify, Activity, Comment, Report, Member, ActivityRequest, Message
from django.contrib.auth.models import User
from frittie.helper.settings_helper import MEMBER_USER_RELATIONS
from frittie.helper.activity_helper import is_upcoming_activity, is_happening_activity
from django.core import serializers 
from frittie.settings import conn
from friends.models import Friendship
import user_streams
import datetime

@dajaxice_register
def join_activity_request(request,activity_id):
	member_login = get_member_login_object(request)
	activity = Activity.objects.get(pk=activity_id)
	activity_request = ActivityRequest.objects.filter(activity=activity,member_join=member_login,member_create=activity.member_create)
	if len(activity_request) != 0:
		activity_request[0].request_status = 'Waiting'
		activity_request[0].save()
	else:	
		new_request = ActivityRequest.objects.create(activity=activity,member_join=member_login,member_create=activity.member_create,request_status='Waiting',date=datetime.datetime.now())
		new_request.save()
	notify_type= 'join_activity_request'
	content = ("<a href='/" + member_login.user.username + "' >" + 
					member_login.user.first_name + " " + member_login.user.last_name + 
				"</a>" + 
				" want to join your activity " + 
				"<a href='/activity/" + str(activity.pk) + "' >" + 
					activity.name + 
				"</a>")
	new_notify = Notify.objects.create(notify_type=notify_type,notify_to=activity.member_create,notify_from=member_login,status='new',date=datetime.datetime.now(),content=content)
	new_notify.save()
	new_buzz_type = len(Notify.objects.filter(notify_to=activity.member_create,status='new'))
	new_mail_type = len(Message.objects.filter(member_receive=activity.member_create,status='new'))
	buzz = simplejson.dumps({'new_notify': new_buzz_type + new_mail_type, 'new_buzz_type': new_buzz_type, 'new_mail_type': new_mail_type, 'username': activity.member_create.user.username})
	conn.send(buzz,destination='/update')
	return simplejson.dumps({})

@dajaxice_register
def cancel_joining_activity(request, activity_id, message):
	member_login = get_member_login_object(request)
	activity = Activity.objects.get(pk=activity_id)
	activity.member_join.remove(member_login)
	activity_request = ActivityRequest.objects.get(activity=activity,member_join=member_login,member_create=activity.member_create)
	activity_request.delete()
	notify_type= 'cancel_joining_activity'
	content = ("<a href='/" + member_login.user.username + "' >" + 
					member_login.user.first_name + " " + member_login.user.last_name + 
				"</a>" + 
				" want to cancel attending your activity " + 
				"<a href='/activity/" + str(activity.pk) + "' >" + 
					activity.name + 
				"</a>." + 
				"\n The reason for this cancel is: \n" + message)
	new_notify = Notify.objects.create(notify_type=notify_type,notify_to=activity.member_create,notify_from=member_login,status='new',date=datetime.datetime.now(),content=content)
	new_notify.save()
	new_buzz_type = len(Notify.objects.filter(notify_to=activity.member_create,status='new'))
	new_mail_type = len(Message.objects.filter(member_receive=activity.member_create,status='new'))
	buzz = simplejson.dumps({'new_notify': new_mail_type + new_buzz_type, 'new_buzz_type':new_buzz_type,'new_mail_type': new_mail_type, 'username': activity.member_create.user.username})
	conn.send(buzz,destination='/update')
	return simplejson.dumps({'activity_id':activity_id})

@dajaxice_register
def recommend_friend(request,activity_id,friends):
	activity = Activity.objects.get(pk=activity_id)
	member_login = get_member_login_object(request)
	members = Member.objects.filter(pk__in=friends)
	#print members
	for member in members:
		if len(Notify.objects.filter(notify_type='recommend_activity',notify_to=member,notify_from=member_login,object_id=activity_id)) == 0:
			notify_type = 'recommend_activity'
			content = ("<a href='/" + member_login.user.username + "' >" + 
							member_login.user.first_name + " " + member_login.user.last_name + 
						"</a>" + 
						" recommend you this activity " + 
						"<a href='/activity/" + str(activity.pk) + "' >" + 
							activity.name + 
						"</a>.")
			new_notify = Notify.objects.create(object_id=activity_id,notify_type=notify_type,status='new',notify_to=member,notify_from=member_login,date=datetime.datetime.now(),content=content)
			new_notify.save()
			new_buzz_type = len(Notify.objects.filter(notify_to=member,status='new'))
			new_mail_type = len(Message.objects.filter(member_receive=member,status='new'))
			buzz = simplejson.dumps({'new_notify': new_mail_type+new_buzz_type,'new_buzz_type':new_buzz_type,'new_mail_type': new_mail_type, 'username': member.user.username})
			conn.send(buzz,destination='/update')
	return simplejson.dumps({})

# This function is checked everytime to see if the activity status change or not
@dajaxice_register
def change_activity_status(request,activity_id):
	activity = Activity.objects.get(pk=activity_id)
	old_status = activity.activity_status
	if is_upcoming_activity(activity_id):
		activity.activity_status = 'Upcoming'
	elif is_happening_activity(activity_id):
		activity.activity_status = 'Happening'
	else:
		activity.activity_status = 'Past'
	activity.save()
	new_status = activity.activity_status
	return simplejson.dumps({'old_status':old_status,'new_status': new_status})

@dajaxice_register
def add_comment(request,activity_id,comment_content):
	member_login = get_member_login_object(request)
	activity = Activity.objects.get(pk=activity_id)
	now = datetime.datetime.now()
	new_comment = Comment.objects.create(comment_type='activity',object_id=activity_id,content=comment_content,member=member_login,created_date=now)
	new_comment.save()
	result = {}
	result['comment_id'] = new_comment.pk
	result['member'] = {'username': member_login.user.username,'first_name':member_login.user.first_name, 'last_name': member_login.user.last_name,'avatar': member_login.avatar.url}
	result['content'] = new_comment.content_html
	result['date'] = new_comment.created_elapse_time
	
	#if request.session['allow_comment_stream']:	
	friend_activity_content = get_stream_content('add_activity_comment','friends_content',{'member_login':member_login,'activity':activity, 'comment': new_comment, 'comment_content':set_fixed_string(new_comment.content,30)})
	user_activity_content = get_stream_content('add_activity_comment','user_content',{'member_login':member_login,'activity':activity})
	list_friends_username = Friendship.objects.friends_of(member_login.user).values_list('username', flat=True)
	user_streams.add_stream_item(member_login.user, friend_activity_content, user_activity_content)
	buzz = simplejson.dumps({'new_friend_activity': friend_activity_content, 'list_friends_username': list(list_friends_username) })
	conn.send(buzz,destination='/update')
	#request.session['allow_comment_stream'] = False
	return simplejson.dumps(result)

@dajaxice_register
def remove_comment(request,comment_id):
	Comment.objects.get(pk=comment_id).delete()
	return simplejson.dumps({'comment_id':comment_id})

@dajaxice_register
def report_comment(request,comment_id):
	comment = Comment.objects.get(pk=comment_id)
	report = Report.objects.filter(report_type='comment',object_id=comment.pk)
	member_login = get_member_login_object(request)
	if len(report) == 0:	
		new_report = Report.objects.create(report_type='comment',object_id=comment.pk,date=datetime.datetime.now())
		new_report.member_report.add(member_login)
		new_report.save()
	else:
		report[0].member_report.add(member_login)
	return simplejson.dumps({'comment_id': comment_id})

@dajaxice_register
def edit_comment(request,comment_id,comment_content):
	member_login = get_member_login_object(request)
	now = datetime.datetime.now()
	comment = Comment.objects.get(pk=comment_id)
	comment.content = comment_content
	comment.edit_date = now
	comment.save()
	result = {}
	result['comment_id'] = comment_id
	result['member'] = {'username': member_login.user.username,'first_name':member_login.user.first_name, 'last_name': member_login.user.last_name,'avatar': member_login.avatar.url}
	result['content'] = comment.content_html
	result['date'] = comment.edit_elapse_time
	return simplejson.dumps(result)

@dajaxice_register
def create_activity(request,location_id):
	return simplejson.dumps({})