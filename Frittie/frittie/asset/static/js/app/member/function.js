function add_friend_callback(data) {
	var new_btn = "<div class='btn-group'>" + 
          				"<button class='btn btn-primary dropdown-toggle' data-toggle='dropdown'>Waiting Response <span class='caret'></span></button>" +
          				"<ul class='dropdown-menu'>" + 
            				"<li><a href='#' id='cancel_btn' onClick='handle_cancel_friend_request()'>Cancel Request</a></li>" + 
          				"</ul>" + 
        		  "</div>"
	$(".friend-btn-area").html(new_btn)
	var s = '<p class="notice-message">Your friend request has been sent to <a href=/' + 
				data['username'] + " >" + data['firstname'] + " " + data['lastname'] + "</a></p>"
	var el = "#show_notice_message"
	show_message(s,el)
	$("#add_friend_link").remove()
}

function unfriend_callback(data) {
	$("#modal_unfriend").modal('hide')
	var new_btn = "<input type='button' id='add_friend_btn' class='btn btn-primary' href='#' value='Add Friend' onClick='handle_add_friend()' />"
	$(".friend-btn-area").html(new_btn)
	var s = '<p class="notice-message">You have been unfriend with <a href=/' + 
				data['username'] + " >" + data['firstname'] + " " + data['lastname'] + "</a></p>"
	var el = "#show_notice_message"
	show_message(s,el)
	if (data['num_friends'] == 0) {
		var gender = get_gender(data['gender'],false) 
		var add_friend_link = 	"<div class='no-friend-notice'>" +
									"<p>" + 
										"<b>" + data['firstname'] + " " + data['lastname'] + "</b> currently have no friends." + 
										"<a href='#' id='add_friend_link' onClick='handle_add_friend()' > Add " + gender + "</a>" + 
									"</p>" + 
								"</div>"
		$('.friends-area-body').html(add_friend_link);
	} 
}

function accept_friend_request_callback(data) {
	if (data['reload'] == 'True') {
		location.reload()
	} else {
		var new_btn = "<input type='button' id='unfriend_btn' class='btn btn-primary' href='#' value='Unfriend' onClick='handle_unfriend_init()' />"
		$(".friend-btn-area").html(new_btn)
		var s = '<p class="notice-message">You are now friend with <a href=/' + 
				data['username'] + " >" + data['firstname'] + " " + data['lastname'] + "</a></p>"
		var el = "#show_notice_message"
		show_message(s,el)
	}
}

function decline_friend_request_callback(data) {
	if (data['reload'] == 'True') {
		location.reload()
	} else {
		var new_btn = "<input type='button' id='add_friend_btn' class='btn btn-primary' href='#' value='Add Friend' onClick='handle_add_friend()' />"
		$(".friend-btn-area").html(new_btn)
		var s = '<p class="notice-message">Your have declined friend request of <a href=/' + 
					data['username'] + " >" + data['firstname'] + " " + data['lastname'] + "</a></p>"
		var el = "#show_notice_message"
		show_message(s,el)
	}
}

function cancel_friend_request_callback(data) {
	if (data['reload'] == 'True') {
		location.reload()
	} else {
		var new_btn = "<input type='button' id='add_friend_btn' class='btn btn-primary' href='#' value='Add Friend' onClick='handle_add_friend()' />"
		$(".friend-btn-area").html(new_btn)
		var s = '<p class="notice-message">Your have cancel your friend request to <a href=/' + 
				data['username'] + " >" + data['firstname'] + " " + data['lastname'] + "</a></p>"
		var el = "#show_notice_message"
		show_message(s,el)
		if ($(".no-friend-notice").length > 0) {
			var gender = get_gender(data['gender'],false) 
			var add_friend_link = "<p>" + 
									"<b>" + data['firstname'] + " " + data['lastname'] + "</b> currently have no friends." + 
									"<a href='#' id='add_friend_link' onClick='handle_add_friend()' > Add " + gender + "</a>" + 
								  "</p>"
			$('.no-friend-notice').html(add_friend_link);
		} 
	}
}

function handle_add_friend() {
	var is_login = $("#check_login").val();
	var member_view_username = $('#member_view_username').val()
	if (is_login == "True"){
        Dajaxice.frittie.app.member.add_friend(add_friend_callback,{'username': member_view_username})
    } else {
        window.location.href = WEBSITE_HOMEPAGE + "/login/?next=/" + member_view_username;
    }
}

function handle_unfriend_init() {
	$("#modal_unfriend").modal('show')
}

function handle_unfriend_complete() {
	var member_view_username = $('#member_view_username').val()
	Dajaxice.frittie.app.member.unfriend(unfriend_callback,{'username': member_view_username})    	
}

function handle_cancel_friend_request() {
	var member_view_username = $('#member_view_username').val()
	Dajaxice.frittie.app.member.cancel_friend_request(cancel_friend_request_callback,{'username': member_view_username})
}

function handle_accept_friend_request() {
	var member_view_username = $('#member_view_username').val()
  	Dajaxice.frittie.app.member.accept_friend_request(accept_friend_request_callback,{'username': member_view_username})
}

function handle_decline_friend_request() {
	var member_view_username = $('#member_view_username').val()
  	Dajaxice.frittie.app.member.decline_friend_request(decline_friend_request_callback,{'username': member_view_username})
}

function add_message_callback(data) {
	$('#modal_send_message').modal('hide')
}

function upload_activity_photo_callback(data) {
	$('#modal_upload_photo').modal('show')
}

function handle_upload_photo(activity_id) {
	Dajaxice.frittie.app.photo.upload_activity_photo(upload_activity_photo_callback,{'activity_id': activity_id})
}

function cancel_joining_callback(data) {
	var el = "#activity_" + data['activity_id'].toString()
  	$(el).slideUp(function(){ jQuery(this).remove(); });
	var s = "<p class='notice-message'>You have canceled your attendance in this activity. Your message has been sent to the host</p>"
	var el = '#show_notice_message'
	show_message(s,el)
}

function handle_cancel_joining_activity(activity_id) {
	$('#modal_cancel_activity').modal('show')
	$('#current_activity_action').val(activity_id);
}

function handle_stream_content(content) {
	for (var i = 0 ; i < content.length; i++) {
		if ((content[i] == '*') && (content[i+1] == '*') && (content[i+2] == '*')) {
			console.log(content.substring(i+3,content.length))
			return content.substring(i+3,content.length)
		}
	}
}

function update_streams(data) {
	var member_login_username = $('#member_login_username').val()
	if (data['list_friends_username']) {
		for (var i = 0; i < data['list_friends_username'].length; i++) {
			if (data['list_friends_username'][i] == member_login_username) {
				var new_item = $(data['new_friend_activity']).hide();
    			$('.friends-activity-stream-list-data').prepend(new_item);
    			new_item.slideDown();
    			break;
			}
		}
	} else {
		var check = false
		for (var i = 0; i < data['list_friends_username1'].length; i++) {
			if (data['list_friends_username1'][i] == member_login_username) {
				var new_item = $(data['new_friend_activity1']).hide();
    			$('.friends-activity-stream-list-data').prepend(new_item);
    			new_item.slideDown();
    			check = true
    			break;
			}
		}
		if (check == false) {
			for (var i = 0; i < data['list_friends_username2'].length; i++) {
				if (data['list_friends_username2'][i] == member_login_username) {
					var new_item = $(data['new_friend_activity2']).hide();
    				$('.friends-activity-stream-list-data').prepend(new_item);
    				new_item.slideDown();
    				break;
				}
			}	
		}
	}
}

/*function list_choose_location(url,el) {
	$.ajax({
    	url:url,
    	type:"GET",
    	accepts:"application/json",
    	dataType:"json",
    	success:function(data){
      		var content = "<ul id='choose-location-list-data'>";
      		for (var i = 0; i < data['objects'].length; i++)
      		{
      			var location = data['objects'][i];
      			content = content + "<li class='choose-location-item-data' onclick='handle_choose_location(" + location['id'] + ")' >" +
      										"<div class='location-name'>" + 
      											"<a href='/location/" + location['id'] + "' >" + location['name'] + "</a>" + 
      										"</div>" +
      										"<div class='location-avatar'>" + 
      											"<img src=" + location['avatar'] + " width=85 height=85/>" + 
      										"</div>" + 
      										"<div class='location-rating'>" + 
      											 "<div class='star-rating' data-rating=" + location['rating'] + " >" + 
      											 "</div>" + 
      										"</div>" + 
      										"<div class='location-address'>" + 
      											location['city'] + ", " + location['state'] + 
      										"</div>" +
      								"</li>";
      		}
      		content = content + "</ul>";
      		$(el).html(content);
      		$(".star-rating").raty({
        		readOnly: true,
        		half  : true,
        		score: function() {
          			return $(this).attr('data-rating');
        		}
      		})
    	}
  	});
}*/

function handle_choose_location(location_id) {
	$('#choose_location_id').val(location_id);
	$('#choose_location_btn').removeClass('disabled')
}

function choose_location_autocomplete(data_src) {
 	var data = new Array(); 
    for (var i = 0; i < data_src.length; i++) {
        var dt = new Object();
        dt.label = data_src[i]['name']
        dt.value = data_src[i]['value']
        dt.description = data_src[i]['description']
        dt.icon = data_src[i]['icon']
        data.push(dt)
    }
    
    $("#search_location_query").autocomplete({
        source: data,
        minLength: 1,
        focus: function( event, ui ) {
            $( "#search_location_query" ).val( ui.item.label );
            return false;
        },
        select: function( event, ui ) {
          $( "#search_location_query" ).val( ui.item.label );
          var find_el = "#choose_" + ui.item.value
          if (is_el_exist(find_el)) {
          	$(find_el).show()
          	$(find_el).parent().prepend($(find_el));
          	$('.choose-location-list-data li').slice(1).hide()
          	$('#choose_location_btn').addClass('disabled')
          } else {
          	$('.choose-location-list-data li').hide()
          	$('#choose_location_btn').addClass('disabled')
          }
        return false;
      }
    })
    .data( "autocomplete" )._renderItem = function( ul, item ) {
        var inner_html = '<a>' + 
                              '<div class="list_item_container">' +
                                '<div class="image"><img src="' + item.icon + '"></div>' +
                                '<div class="label">' + item.label + '</div>' +
                                '<div class="description">' + item.description + '</div>' +
                              '</div>' +
                          '</a>';
        return $( "<li></li>" )
        .data( "item.autocomplete", item )
        .append(inner_html)
        .appendTo( ul );
    };
}

function load_location_callback(data) {
	var content = "<ul class='choose-location-list-data'>";
    for (var i = 0; i < data.length; i++)
    {
    	var location_id = data[i]['pk']
      	var location = data[i]['fields'];
      	content = content + "<li class='choose-location-item-data' id='choose_location_" + location_id + "' onclick='handle_choose_location(" + location_id + ")' >" +
      								"<div class='location-name'>" + 
      									"<a href='/location/" + location_id + "' >" + location['name'] + "</a>" + 
      								"</div>" +
      								"<div class='location-avatar'>" + 
      									"<img src=" + WEBSITE_HOMEPAGE + "/asset/media/" + location['avatar'] + " width=85 height=85/>" + 
      								"</div>" + 
      								"<div class='location-rating'>" + 
      									 "<div class='star-rating' data-rating=" + location['rating'] + " >" + 
      									 "</div>" + 
      								"</div>" + 
      								"<div class='location-address'>" + 
      									location['city'] + ", " + location['state'] + 
     								"</div>" +
      						"</li>";
    }
    content = content + "</ul>";
    $(".choose-location-display").html(content);
	$(".star-rating").raty({
        readOnly: true,
        half  : true,
        score: function() {
          	return $(this).attr('data-rating');
        }
    })
	$('#modal_choose_location').modal('show')	
}

function compare_age(el1,el2) {
    var small = parseInt($(el1).val())
    var big = parseInt($(el2).val())
    if (small > big) {
        $(el1).val(big-1)
    }
}

function validate_field(invalid_el,el_error_exist,main_el,error_el,process,error_display) {
    if (invalid_el) {
          if (!el_error_exist) {
              $(main_el).append(error_display)
          }
          process = false
      } else {
          var remove_el = main_el + " " + error_el
          //console.log(remove_el)
          if (el_error_exist) $(remove_el).remove()
      }
    console.log(process)
    return process
}