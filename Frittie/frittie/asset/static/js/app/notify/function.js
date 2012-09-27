function accept_friend_request_callback(data) {
	if (data['reload'] == 'True') {
		console.log('true')
		location.reload()
	} else {
		var new_content = data['new_content']
		var notify_el = "#notify-" + data['notify_id']
		$(notify_el).find('.notify-content').html(new_content)
		var s = '<p class="notice-message">You are now friend with <a href=/' + 
				data['username'] + " >" + data['firstname'] + " " + data['lastname'] + "</a></p>"
		var el = "#show_notice_message"
		show_message(s,el)
	}
}

function decline_friend_request_callback(data) {
	if (data['reload'] == 'True') {
		console.log('true1')
		location.reload()
	} else {
		var new_content = data['new_content']
		var notify_el = "#notify-" + data['notify_id']
		$(notify_el).find('.notify-content').html(new_content)
		var s = '<p class="notice-message">Your have declined friend request of <a href=/' + 
				data['username'] + " >" + data['firstname'] + " " + data['lastname'] + "</a></p>"
		var el = "#show_notice_message"
		show_message(s,el)
	}
}

function handle_accept_friend_request(notify_id) {
	var notify_el = "#get_username_notify" + notify_id.toString()
	var username = $(notify_el).val()
	Dajaxice.frittie.app.notify.accept_friend_request(accept_friend_request_callback,{'username': username,'notify_id': notify_id})
}

function handle_decline_friend_request(notify_id) {
	var notify_el = "#get_username_notify" + notify_id.toString()
	var username = $(notify_el).val()
	Dajaxice.frittie.app.notify.decline_friend_request(decline_friend_request_callback,{'username': username,'notify_id': notify_id})
}