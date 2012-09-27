from frittie.app.main.models import Member, Message
from django.http import HttpResponse, HttpResponseRedirect
from frittie.helper.common_helper import set_fixed_string, get_member_login_object, check_user_block
from django.db.models import Q

def get_all_conversation(request):
	member_login = get_member_login_object(request)
	list_member_chat, list_last_chat_message, list_last_chat_date, result = [], [], [], []
	new_messages = Message.objects.filter( (Q(member_receive=member_login) | Q(member_send=member_login)), Q(status='new'))
	for new_message in new_messages:
		new_message.status= 'old'
		new_message.save()
	messages = Message.objects.filter(Q(member_receive=member_login) | Q(member_send=member_login)).order_by('-date')
	for message in messages:
		if message.member_send != member_login and message.member_send not in list_member_chat: 
			list_member_chat.append(message.member_send)
			list_last_chat_message.append(set_fixed_string(message.content,60))
			list_last_chat_date.append(message.elapse_time)
		if message.member_receive != member_login and message.member_receive not in list_member_chat: 
			list_member_chat.append(message.member_receive)
			list_last_chat_message.append("<i class='icon-share-alt'></i>" + set_fixed_string(message.content,60))
			list_last_chat_date.append(message.elapse_time)
	for i in range(0,len(list_member_chat)):
		if check_user_block(member_login.user,list_member_chat[i].user) == False:
			data = {'member': list_member_chat[i],'last_chat': list_last_chat_message[i],'date': list_last_chat_date[i]}
			result.append(data)
	return result


def get_specific_conversation(request,member_chat):
	member_login = get_member_login_object(request)
	if check_user_block(member_login.user,member_chat.user):
		return 'redirect'
	new_messages = Message.objects.filter((Q(member_send=member_login,member_receive=member_chat) | Q(member_send=member_chat,member_receive=member_login)), Q(status='new'))
	for new_message in new_messages:
		new_message.status= 'old'
		new_message.save()
	messages = list(Message.objects.filter(Q(member_send=member_login,member_receive=member_chat) | Q(member_send=member_chat,member_receive=member_login)).order_by('date'))
	return messages

