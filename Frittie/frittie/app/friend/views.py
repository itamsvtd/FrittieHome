from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.utils import simplejson
from django.core import serializers
from django.contrib.auth.decorators import login_required
from frittie.helper.common_helper import get_member_login_object, get_autocomplete_data, get_new_buzzes, get_new_mail
from frittie.helper.friend_helper import get_facebook_friends
from frittie.helper.activity_helper import get_today_activity, get_trending_activity, get_hot_activity
from frittie.app.main.models import Member, Location, LocationCategory

@login_required()
def find_friend(request):
	member_login = get_member_login_object(request)
	autocomplete_data = get_autocomplete_data(request)
	is_import_fb_friend = False
	invite_friends = None
	suggest_friends = None
	facebook_friends = get_facebook_friends(member_login)
	new_buzzes = get_new_buzzes(request)
	new_mail = get_new_mail(request)
	new_notify = len(new_buzzes) + len(new_mail)
	if facebook_friends != None:
		is_import_fb_friend = True
		invite_friends = facebook_friends[1]
		suggest_friends = facebook_friends[0]
	return render_to_response('friend_template/page/main_page.html',
							{
								"member_login": member_login,
								"autocomplete_data": autocomplete_data,
								'is_import_fb_friend': is_import_fb_friend,
								'invite_friends': invite_friends,
								'suggest_friends': suggest_friends,
								'new_notify': new_notify,
								'new_buzzes': new_buzzes,
								'new_mail': new_mail
							},
							context_instance=RequestContext(request)
							)
