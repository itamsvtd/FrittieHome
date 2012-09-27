###############################
#  Author: Dang Nguyen        #
#  Date: 5/24/2012            #
#  Last Modified: 5/29/2012   #
###############################

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.utils import simplejson
from django.core import serializers
from frittie.helper.common_helper import get_member_login_object, get_autocomplete_data, get_new_buzzes, get_new_mail
from frittie.helper.activity_helper import get_today_activity, get_trending_activity, get_hot_activity
from frittie.app.main.models import Member, Location, LocationCategory

def main_page(request):
	autocomplete_data = get_autocomplete_data(request)
	location_categories = LocationCategory.objects.all()
	member_login = get_member_login_object(request)
	new_buzzes = get_new_buzzes(request)
	new_mail = get_new_mail(request)
	new_notify = len(new_buzzes) + len(new_mail)
	locations = Location.objects.all()
	today_activities = get_today_activity()
	trending_activities = get_trending_activity()
	hot_activities = get_hot_activity()
	return render_to_response(
			"main_template/page/index.html",
			{
				"member_login": member_login,
				'new_notify': new_notify,
				'new_buzzes': new_buzzes,
				'new_mail': new_mail,
				"locations": locations,
				"autocomplete_data": autocomplete_data,
				"location_categories": location_categories,
				"today_activities": today_activities,
				'trending_activities': trending_activities,
				'hot_activities': hot_activities,
			},
			context_instance=RequestContext(request)
		)

# This will show a general page for all kind of error
def show_error(request):
	error_type = None
	if error_type in request.GET:
		error_type = request.GET['type']

	autocomplete_data = get_autocomplete_data(request)
	member_login = get_member_login_object
	new_buzzes = get_new_buzzes(request)
	new_mail = get_new_mail(request)
	new_notify = len(new_buzzes) + len(new_mail)
	return render_to_response(
				"error.html",
				{
					"member_login": member_login,
					'error_type': error_type,
					'new_notify': new_notify,
					'new_buzzes': new_buzzes,
					'new_mail': new_mail,
				},
				context_instance=RequestContext(request)
				)