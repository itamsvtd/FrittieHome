import re

from django.contrib.auth.models import User
from settings_helper import SESSION_KEY, KEYWORD_URL
from django.utils.translation import ugettext_lazy as _, ugettext
from allauth.utils import email_address_exists
from emailconfirmation.models import EmailAddress
from frittie.app.main.models import Member
from friends.models import FriendshipRequest, Friendship
from django.shortcuts import get_object_or_404
import user_streams

alnum_re = re.compile(r"^\w+$")


# Helper for member app. Input: dtn1712@gmail.com -> Output: dtn1712
def get_prefix_email(email):
	result = ""
	for i in range(0,len(email)):
		if email[i] == "@":
			break
		result = result + email[i]
	return result.replace('.','_')

# Set a readable username created from analyze the first name, last name
# and email. Use this when create new member since it is just required
# user to enter email for registration, not username
def set_readable_username(email):
	name = get_prefix_email(email)
	u = User.objects.filter(username=name)
	if len(u) == 0:
		return name
	else:
		i = 1
		while len(u) != 0:
			test_username = name + str(i)
			u = User.objects.filter(username=test_username)
			if len(u) == 0: 
				return test_username
			i = i + 1

# Check if there are any user login in the page -> This is currently replaced by 
# get_member_login_object in the common_helper.py
def check_user_login_page(request,username):
	if SESSION_KEY in request.session:
		user_id = request.session[SESSION_KEY]
		user_login = User.objects.get(pk=user_id)
		if user_login.username == username:
			return True
		else:
			return False
	else:
		return False

# This is used for settings function to validate the username
# Value:
#		-1 ->  user contain incorrect symbol
#		 0 ->	user already exist
#		 1 ->	good
def validate_username_setting(request):
	value = request.POST["username"]
	username = User.objects.get(pk=request.session[SESSION_KEY]).username
	if not alnum_re.search(value):
		return -1
	if value != username:
		try:
			User.objects.get(username__iexact=value)
		except User.DoesNotExist:
			return 1
		return 0
	else:
		return 1

# This is used for settings function to validate the email
# Value:
#	 -1 -> exist
#	  1 -> not exist
def validate_email_setting(request):
	value = request.POST['email']
	print value
	email = User.objects.get(pk=request.session[SESSION_KEY]).email
	print email
	if value != email:
		if value and email_address_exists(value):
			return -1
		else:
			return 1
	else:
		return 1

# Check if the current login user is friend with this user
def check_friendship(request,username):
	if SESSION_KEY in request.session:
		user1 = User.objects.get(pk=request.session[SESSION_KEY])
		user2 = get_object_or_404(User, username=username)
		fr1 = FriendshipRequest.objects.filter(from_user=user1,to_user=user2,accepted=False)
		if len(fr1) == 0:
			fr2 = FriendshipRequest.objects.filter(from_user=user2,to_user=user1,accepted=False)
			if len(fr2) == 0:
				fs = Friendship.objects.are_friends(user1,user2)
				if fs: return "Is_friend"
				else: return "Not_friend"
			else:
				return "Response"
		else:
			return "Waiting"
	else:
		return "Not_friend"

# Check if the user has confirmed email yet
def check_confirm_email(request):
	user = User.objects.get(pk=request.session[SESSION_KEY])
	try:
		if EmailAddress.objects.get(user=user).verified:
			return True
		else:
			return False
	except:
		return False

# Friends' activity. Show in the admin page
def get_friend_activity_stream(request,content_type):
	if SESSION_KEY in request.session:
		user = User.objects.get(pk=request.session[SESSION_KEY])
		member = Member.objects.get(user=user)
		friends = member.get_friends()
		print "friend: "
		print friends
		obj_list = []
		for friend in friends:
			items = user_streams.get_stream_items(friend.user)
			for item in items:
				if member.user.username not in item.user_exclude:
					data = {}
					data['user'] = friend
					if content_type == 'friend_content':
						data['friend_content'] = item.friend_content
					elif content_type == "page_content":
						data['page_content'] = item.page_content
					data['time'] = item.created_at
					obj_list.append(data)
		obj_list.sort(key=lambda r: r['time'],reverse=True)
		return obj_list
	return []