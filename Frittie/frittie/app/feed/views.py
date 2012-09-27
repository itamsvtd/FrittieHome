from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.utils import simplejson
from django.core import serializers
from django.contrib.auth.decorators import login_required
from frittie.helper.common_helper import get_member_login_object, get_autocomplete_data, get_new_buzzes, get_new_mail
from frittie.helper.member_helper import get_friend_activity_stream
from frittie.app.main.models import Member
from frittie.settings import PAGE_STREAM_LIMIT

@login_required()
def show_feeds(request):
	member_login = get_member_login_object(request)
	autocomplete_data = get_autocomplete_data(request)
	friends = member_login.get_friends()
	friends_activity_stream = get_friend_activity_stream(request,'page_content')[:PAGE_STREAM_LIMIT]
	new_buzzes = get_new_buzzes(request)
	new_mail = get_new_mail(request)
	new_notify = len(new_buzzes) + len(new_mail)
	return render_to_response('feed_template/page/main_page.html',
							{
								"member_login": member_login,
								"autocomplete_data": autocomplete_data,
								'friends': friends,
								'friends_activity_stream':friends_activity_stream,
								'new_notify': new_notify,
								'new_buzzes': new_buzzes,
								'new_mail': new_mail
							},
							context_instance=RequestContext(request)
							)