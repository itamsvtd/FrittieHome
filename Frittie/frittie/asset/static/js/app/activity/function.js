function strip_comment_whitespace(content) {
  var first_pos, last_pos;
  for (var i = 0; i < content.length; i++) {
    if ((content.charAt(i) != " ") && (content.charAt(i) != "\n")) {
        first_pos = i
        break
    }
  }
  for (var i = content.length-1; i > 0; i--) {
    if ((content.charAt(i) != " ") && (content.charAt(i) != "\n")) {
        last_pos = i+1
        break
    }
  }
  return content.substring(first_pos,last_pos)
}

function handle_comment_html_tag(content) {
	return strip_comment_whitespace(content.replace(/<br>/gi,"\n").replace(/(<([^>]+)>)/ig,"").replace(/&nbsp;/g,' ').replace(/\t/g,''));
}

// Callback function from ajax handle the add comment process. This is completed
function add_comment_callback(data) {
	var s =	"<li class='comment-item-data' id='comment-" + data['comment_id'] + "' >" +
					"<div class='remove-comment pull-right'>" +
						"<a href='#comment-box' class='icon-remove' id='remove_comment_btn' rel='tooltip' title='Remove this comment' onclick='init_remove_comment(" + data['comment_id'] + ")' ></a>" + 
					"</div>" +
					"<div class='edit-comment pull-right'>" +
						"<a href='#comment-box' class='icon-pencil' id='edit_comment_btn' rel='tooltip' title='Edit this comment' onclick='init_edit_comment(" + data['comment_id'] + ")'></a>" +
					"</div>" + 
					"<div class='comment-member'>" + 
						"<a href='/" + data['member']['username'] + "' >" + 
							"<img src=" + data['member']['avatar'] + " width=50 height=50>" + 
							"<p>" +
								data['member']['first_name'] + " " + data['member']['last_name'] + 
							"</p>" + 
						"</a>" + 
					"</div>" +
					"<div class='comment-main-content'>" +
						"<p>" + 
							data['content'] +
						"</p>" +
					"</div>" +
					"<div class='comment-post-date'>" +
						"<p>" + 
							data['date'] + 
						"</p>" + 
					"</div>" +						
				"</li>";
	var new_item = $(s).hide();
	$('.comment-list-data').append(new_item);
	new_item.slideDown();
	$('#comment_box').val("")
}

function edit_comment_callback(data) {
	var comment_el = "#comment-" + data['comment_id']
	var new_content = "<p>" + data['content'] + "</p>"
	var update_date = "<div class='comment-edit-date'>" + 
							"<p><small>Last Updated: " + 
									data['date'] +  
								"</small>" + 
							"</p>" + 
						"</div>"
	$(comment_el).find('.comment-main-content').html(new_content)
	if ($(comment_el).find('.comment-edit-date').length == 0) {
		$(comment_el).append(update_date)
	} else {
		$(comment_el).find('.comment-edit-date').html(update_date)	
	}
}

// Remove comment callback function. This is completed
function remove_comment_callback(data) {
	$("#modal_remove_comment").modal('hide')
	var el = "#comment-" + data['comment_id'].toString()
	$(el).slideUp(function(){ jQuery(this).remove(); });
}

// Report comment callback function. This is completed
function report_comment_callback(data) {
	alert('Thank you for your report. We will investigate and have an appropriate action')
}

// Remove comment handle function. This is completed
function init_remove_comment(comment_id) {
	$("#current_comment").val(comment_id.toString())
	$("#modal_remove_comment").modal('show')
} 

function final_remove_comment() {
	var comment_id = parseInt($("#current_comment").val(),10);
	Dajaxice.frittie.app.activity.remove_comment(remove_comment_callback,{'comment_id': comment_id}, {'error_callback': custom_error})
}
// Report comment handle function. This is completed
function report_comment(comment_id) {
    var is_login = $("#check_login").val();
    var activity_id = $("#activity_id").val();
	if (is_login == "True"){
       	Dajaxice.frittie.app.activity.report_comment(report_comment_callback,{'comment_id': comment_id}, {'error_callback': custom_error})
    } else {
       	window.location.href = WEBSITE_HOMEPAGE + "/login/?next=/activity/" + activity_id;
    }
}

function final_edit_comment(e) {
	var comment_id = $("#current_comment").val()
	if (e.which == 13 && e.shiftKey) {
           var content = this.value;
           var caret = getCaret(this);
           this.value = content.substring(0,caret);
           e.stopPropagation();
    } 
    // Enter key action. Handle the comment here
    else if (e.which == 13) {
    	var comment_box_id = "#edit_comment_" + comment_id.toString() + "_box"
    	var comment_content = $(comment_box_id).val();
        if (strip_whitespace(comment_content).length != 0) {
       		Dajaxice.frittie.app.activity.edit_comment(edit_comment_callback,
       			{'comment_id': comment_id, 'comment_content': comment_content}, {'error_callback': custom_error})
        } else {
        	return false;
    	}
    }	
}

function init_edit_comment(comment_id) {
	$("#current_comment").val(comment_id.toString())
	var comment_box_id = "edit_comment_" + comment_id.toString() + "_box"
	var comment_el = "#comment-" + comment_id.toString();
	var content = $(comment_el).find('.comment-main-content').html()
	var correct_content = handle_comment_html_tag(content)
	var s = "<textarea id=" + comment_box_id + " onkeypress='final_edit_comment(event)'>" + correct_content + "</textarea>"
	$(comment_el).find('.comment-main-content').html(s)
}

function join_activity_callback(data) {
	var waiting = "<input type='button' class='btn btn-primary disabled activity-waiting' href='#' value='Waiting Response'>"
	$(".handler-button").html(waiting);
	var s = "<p class='notice-message'>Your request has been sent to the host. Please wait for his/her response</p>"
	var el = '#show_notice_message'
	show_message(s,el)
}

function cancel_joining_callback(data) {
	$(".activity-accepted").remove();
	$("#join_handler").val("Join");
	var s = "<p class='notice-message'>You have canceled your attendance in this activity. Your message has been sent to the host</p>"
	var el = '#show_notice_message'
	show_message(s,el)
}

function recommend_friend_callback(data) {
	$("#modal_friend").modal('hide');
	$('#modal_friend input[type=checkbox]').attr('checked', false);
	var s = '<p class="notice-message">Your recommendation has been sent to your friends</p>'
	var el = '#show_notice_message'
	show_message(s,el)
}

function upload_activity_photo_callback(data) {
	$('#modal_upload_photo').modal('show')
}

function update_streams_callback(data) {
	
}

function handle_choose_location(activity_type) {
	console.log(activity_type)
}

/*******************************************
*										   *	
*	  FUNCTION FOR GOOGLE MAP DIRECTION    * 
*	  Status: Not completed				   *
*										   *
*******************************************/
function initializeGoogleMap() {
  var myOptions = {
    zoom: 13,
    center: new google.maps.LatLng(-34.397, 150.644),
    mapTypeId: google.maps.MapTypeId.ROADMAP
  }
  var map = new google.maps.Map(document.getElementById("location_map"), myOptions);
}

function loadGoogleMapScript() {
  var script = document.createElement("script");
  script.type = "text/javascript";
  script.src = "http://maps.googleapis.com/maps/api/js?key=AIzaSyB_6s_oHHrHt-cYENva4aiMDWCRM_4RtHo&sensor=false&callback=initializeGoogleMap";
  document.body.appendChild(script);
}

