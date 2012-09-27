$(document).ready(function () {
	var el = "#search_friend_query"
	var is_login = $("#check_login").val();

	friends_search_autocomplete(friends_autocomplete_data,el)

  	$("#reply_btn").click(function() {
      	var member_chat_username = $("#member_chat_username").val();
      	var message_content = $("#chat_box").val()
      	if (strip_whitespace(message_content).length != 0) {
      		Dajaxice.frittie.app.message.add_message(add_message_callback,{'username': member_chat_username, 'message': message_content})
  		} else {
  			return false;
  		}
  	});
})