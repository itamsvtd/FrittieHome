from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
from frittie.helper.common_helper import get_member_login_object, get_JSON_exclude_fields, get_stream_content, set_fixed_string
from frittie.app.main.models import Location, Member, Notify, Comment, Report, Message, FritLocation
from frittie.helper.settings_helper import MEMBER_USER_RELATIONS
from django.core import serializers
from frittie.settings import conn 
from friends.models import Friendship
from django.contrib.auth.models import User
import datetime
import user_streams

@dajaxice_register
def follow_location(request,location_id):
	member_login = get_member_login_object(request)
	location = Location.objects.get(pk=location_id)
	location.follow_by.add(member_login)
	friend_activity_content = get_stream_content('follow_location','friends_content',{'member_login':member_login,'location':location})
	user_activity_content = get_stream_content('follow_location','user_content',{'member_login':member_login,'location':location})
	list_friends_username = Friendship.objects.friends_of(member_login.user).values_list('username', flat=True)
	user_streams.add_stream_item(member_login.user, friend_activity_content, user_activity_content)
	buzz = simplejson.dumps({'new_friend_activity': friend_activity_content, 'list_friends_username': list(list_friends_username) })
	conn.send(buzz,destination='/update')
	return simplejson.dumps({'username': member_login.user.username, 'name': member_login.user.first_name + " " + member_login.user.last_name, 'avatar': member_login.avatar.url})

@dajaxice_register
def unfollow_location(request,location_id):
	member_login = get_member_login_object(request)
	location = Location.objects.get(pk=location_id)
	location.follow_by.remove(member_login)
	return simplejson.dumps({'username': member_login.user.username })

@dajaxice_register
def recommend_friend(request,location_id,friends):
	location = Location.objects.get(pk=location_id)
	member_login = get_member_login_object(request)
	members = Member.objects.filter(pk__in=friends)
	for member in members:
		if len(Notify.objects.filter(notify_type='recommend_location',notify_to=member,notify_from=member_login,object_id=location_id)) == 0:
			notify_type = 'recommend_location'
			content = ( "<a href='/" + member_login.user.username + "' >" + 
							member_login.user.first_name + " " + member_login.user.last_name + 
						"</a> " + 
						" recommend you this location " + 
						"<a href='/location/" + str(location.pk) + "' >" + 
							location.name + 
						"</a>.")
			new_notify = Notify.objects.create(object_id=location_id,notify_type=notify_type,status='new',notify_to=member,notify_from=member_login,date=datetime.datetime.now(),content=content)
			new_notify.save()
			new_buzz_type = len(Notify.objects.filter(notify_to=member,status='new'))
			new_mail_type = len(Message.objects.filter(member_receive=member,status='new'))
			buzz = simplejson.dumps({'new_notify': new_mail_type+new_buzz_type,'new_buzz_type':new_buzz_type,'new_mail_type': new_mail_type, 'username': member.user.username})
			conn.send(buzz,destination='/update')
	return simplejson.dumps({})

@dajaxice_register
def rate_location(request):
	return simplejson.dumps({})

@dajaxice_register
def add_comment(request,location_id,comment_content):
	member_login = get_member_login_object(request)
	location = Location.objects.get(pk=location_id)
	now = datetime.datetime.now()
	new_comment = Comment.objects.create(comment_type='location',object_id=location_id,content=comment_content,member=member_login,created_date=now)
	new_comment.save()
	result = {}
	result['comment_id'] = new_comment.pk
	result['member'] = {'username': member_login.user.username,'first_name':member_login.user.first_name, 'last_name': member_login.user.last_name,'avatar': member_login.avatar.url}
	result['content'] = new_comment.content_html
	result['date'] = new_comment.created_elapse_time
	
	#if request.session['allow_comment_stream']:
	friend_activity_content = get_stream_content('add_location_comment','friends_content',{'member_login':member_login,'location':location, 'comment': new_comment, 'comment_content': set_fixed_string(new_comment.content,30)})
	user_activity_content = get_stream_content('add_location_comment','user_content',{'member_login':member_login,'location':location})
	list_friends_username = Friendship.objects.friends_of(member_login.user).values_list('username', flat=True)
	user_streams.add_stream_item(member_login.user, friend_activity_content, user_activity_content)
	buzz = simplejson.dumps({'new_friend_activity': friend_activity_content, 'list_friends_username': list(list_friends_username) })
	conn.send(buzz,destination='/update')
	#request.session['allow_comment_stream'] = False
	
	return simplejson.dumps(result)

@dajaxice_register
def remove_comment(request,comment_id):
	comment = Comment.objects.get(pk=comment_id)
	comment.delete()
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
def load_location(request,location_name,location_type,location_special):
	if location_name:
		return serializers.serialize('json',Location.objects.filter(name__icontains=location_name))
	result = []
	location_type_data = Location.objects.all()
	if location_type != 'All':
		location_type_data = Location.objects.filter(category=location_type)
	if location_special == 'most_rated':
		result = serializers.serialize('json',location_type_data.order_by('-rating')[:30])
	elif location_special == "trending":
		result = serializers.serialize('json',location_type_data.order_by('-comment_amount')[:30])
	elif location_special == 'recommended':
		result = serializers.serialize('json',location_type_data.order_by('-recommend_amount')[:30])	
	return result


@dajaxice_register
def addfritlocationnumber(request,location_id):
	locationf = Location.objects.get(pk=location_id)
	member_login = get_member_login_object(request)
	flocations = FritLocation.objects.filter(location= locationf)
	clocations = FritLocation.objects.filter(location= locationf, memberfrit = member_login)
	if len(clocations)==0 :
		current = len(flocations)+1
		new_frit = FritLocation.objects.create(memberfrit = member_login,fritnum= current, location=locationf)
		new_frit.save()
	else:
		current = "You have already fritted !!"
	return simplejson.dumps({'current':current})

@dajaxice_register
def removefritlocationnumber(request,location_id):
	locationf = Location.objects.get(pk=location_id)
	member_login = get_member_login_object(request)
	flocation = FritLocation.objects.filter(location= locationf, memberfrit = member_login)
	tmp = 0
	if len(flocation)>0:
		for x in flocation:
			tmp = x.fritnum
			break
	mlocations = FritLocation.objects.filter(fritnum__gt=tmp)
	for x in mlocations:
		num = x.fritnum
		FritLocation.objects.filter(fritnum= num).update(fritnum= num -1 )	
	FritLocation.objects.filter(location= locationf, memberfrit = member_login).delete()
	current = "Unfritted successfully"
	return simplejson.dumps({'current':current})