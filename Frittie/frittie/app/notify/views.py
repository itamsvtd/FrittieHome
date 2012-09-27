from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.contrib.auth.models import User
from django.core import serializers
from frittie.app.main.models import Notify
from frittie.helper.common_helper import get_member_login_object, get_new_mail, get_new_buzzes, get_autocomplete_data
from django.contrib.auth.decorators import login_required
from frittie.app.main.utils import get_elapse_time
import datetime

@login_required()
def show_notification(request):
	now = datetime.datetime.now()
	autocomplete_data =  get_autocomplete_data(request)
	member_login = get_member_login_object(request)
	current_page = 1
	if 'page' in request.GET:
		current_page = int(request.GET['page'])
	all_notifies = Notify.objects.filter(notify_to=member_login).order_by("-date")
	last_page = int(len(all_notifies) / 10) + 1
	notifies = all_notifies[(current_page-1)*10:current_page*10] 
	for notify in notifies:
		elapse_time = now - notify.date
		notify.elapse_time = get_elapse_time(int(elapse_time.total_seconds())) 
		if notify.status == 'new': notify.status = 'old'
		notify.save()
	new_buzzes = get_new_buzzes(request)
	new_mail = get_new_mail(request)
	new_notify = len(new_buzzes) + len(new_mail)
	return render_to_response(
			"notify_template/page/main_page.html",
			{
				"autocomplete_data": autocomplete_data,
				"member_login": member_login,
				'current_page': current_page,
				'last_page': last_page,
				"notifies": notifies,
				"new_buzzes": new_buzzes,
				'new_mail': new_mail,
				'new_notify': new_notify
			},
			context_instance=RequestContext(request)
		)
