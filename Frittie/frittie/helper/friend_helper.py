from django.contrib.auth.models import User
from django.core import serializers
from frittie.app.main.models import Member
from django.utils import simplejson
from friends.models import Friendship
from django_facebook.models import FacebookUser

# Suggest fb friend mean friend who already sign up 
# on frittie by using fb account but haven't been friend 
# on frittie
def get_facebook_friends(member_login):
	facebook_friends = FacebookUser.objects.filter(user_id=member_login.user.pk)
	if len(facebook_friends) == 0:
		return None
	else:
		suggest_friend = []
		invite_friend = []
		for friend in facebook_friends:
			try:
				member_friend = Member.objects.get(facebook_id=friend.facebook_id)
				if Friendship.objects.are_friends(member_login.user,member_friend.user) == False:
					suggest_friend.append(friend)
			except:
				invite_friend.append(friend)
		return [suggest_friend,invite_friend]