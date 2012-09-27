# Views for the main app
from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from frittie.app.main.models import Member, Message
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.db.models import Q
from frittie.helper.common_helper import get_new_buzzes, get_friends_autocomplete_data, get_autocomplete_data, get_member_login_object, get_new_mail
from frittie.helper.message_helper import get_all_conversation, get_specific_conversation
from django.contrib.auth.decorators import login_required
from frittie.settings import conn
import datetime

@login_required
def message_main_view(request):
	autocomplete_data = get_autocomplete_data(request)

	member_login = get_member_login_object(request)
	friends = member_login.get_friends()
	friends_autocomplete_data = get_friends_autocomplete_data(request,message=True)
	messages = get_all_conversation(request)
	new_buzzes = get_new_buzzes(request)
	new_mail = get_new_mail(request)
	new_notify = len(new_buzzes) + len(new_mail)
	return render_to_response('message_template/page/main_page.html',
						{
							'autocomplete_data': autocomplete_data,
							'member_login': member_login,
							'new_buzzes': new_buzzes,
							'new_mail': new_mail,
							'new_notify': new_notify,
							'friends': friends,
							'friends_autocomplete_data': friends_autocomplete_data,
							'messages': messages 
						},
						context_instance=RequestContext(request)
					)

@login_required
def member_message(request,username):
	member_chat = get_object_or_404(Member,user=get_object_or_404(User,username=username))
	member_login = get_member_login_object(request)
	messages = get_specific_conversation(request,member_chat)
	if member_chat == member_login or messages == 'redirect': 
		return HttpResponseRedirect('/messages/')

	autocomplete_data = get_autocomplete_data(request)
	friends = member_login.get_friends()
	friends_autocomplete_data = get_friends_autocomplete_data(request,message=True)
	new_buzzes = get_new_buzzes(request)
	new_mail = get_new_mail(request)
	new_notify = len(new_buzzes) + len(new_mail)
	return render_to_response('message_template/page/member_message_page.html',
						{
							'autocomplete_data': autocomplete_data,
							'member_login': member_login,
							'member_chat': member_chat,
							'friends': friends,
							'friends_autocomplete_data': friends_autocomplete_data,
							'new_buzzes': new_buzzes,
							'new_mail': new_mail,
							'new_notify': new_notify,
							'messages': messages
						},
						context_instance=RequestContext(request)
					)

