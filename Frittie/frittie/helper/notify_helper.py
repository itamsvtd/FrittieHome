from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.db.models import Q
from django.core import serializers
from settings_helper import USER_COMMON_INCLUDE_FIELDS, SESSION_KEY
from frittie.app.main.models import Member, Notify, Location, Message, Activity
from django.utils import simplejson
from friends.models import UserBlocks
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
import collections
import datetime

def get_notify_content(notify_type,context_data):
	template_name = 'text/notify/' + notify_type + ".txt"
	return render_to_string(template_name,context_data)
