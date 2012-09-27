from dajax.core import Dajax
from django.http import HttpResponseRedirect
from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
from frittie.helper.common_helper import get_member_login_object, get_JSON_exclude_fields
from frittie.app.main.models import Location, Notify, Member, Message
from frittie.helper.settings_helper import MEMBER_USER_RELATIONS
from friends.models import FriendshipRequest, Friendship
from django.contrib.auth.models import User
from frittie.settings import conn
import datetime

@dajaxice_register
def add_message(request,username,message):
	now = datetime.datetime.now()
	member_chat = Member.objects.get(user=User.objects.get(username=username))
	member_login = get_member_login_object(request)
	new_message = Message.objects.create(member_send=member_login,member_receive=member_chat,content=message,date=now,status='new')
	new_message.save()
	new_buzz_type = len(Notify.objects.filter(notify_to=member_chat,status='new'))
	new_mail_type = len(Message.objects.filter(member_receive=member_chat,status='new'))
	buzz = simplejson.dumps({'new_notify': new_buzz_type + new_mail_type, 'new_buzz_type': new_buzz_type,'new_mail_type': new_mail_type, 'username': member_chat.user.username, 'member_send_username': member_login.user.username, 'member_send_name': member_login.user.first_name + " " + member_login.user.last_name, 'member_send_avatar': member_login.avatar.url, 'msg_content': new_message.content_html, 'date': new_message.elapse_time})
	conn.send(buzz,destination='/update')
	return simplejson.dumps({'message':'Success'})

