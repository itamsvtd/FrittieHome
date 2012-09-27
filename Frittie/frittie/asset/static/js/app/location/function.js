// List activity by using API
function list_activity(url,el) {
	$.ajax({
    	url:url,
    	type:"GET",
    	accepts:"application/json",
    	dataType:"json",
    	success:function(data){
    		var content = "<ul class='activity-data-list'>";
      		for (var i = 0; i < data['objects'].length; i++)
      		{
      			var activity = data['objects'][i];      		
            var member_create = activity['member_create'];	
            var user_create = member_create['user'];
            var member_follow = activity['member_follow'];
            var location = activity['location'];
      			content = content + "<li>" + 
      									"<div class='activity-name'>" + 
                            "<a href='/activity/" + activity['id'] + "' >" + activity['name'] + "</a>" + 
                        "</div>" +                        
      									"<div class='activity-user-create pull-right'><a href='/" + user_create['username'] + "' >" + 
                                  "<img src=" + handle_user_avatar(member_create['avatar'],member_create['gender']) + " width=40 height=40 />" + 
                                  user_create['first_name'] + " " + user_create['last_name'] + "</a>" + 
                        "</div>" + 
                        "<div class='activity-time'>" + 
                            "When: " + handle_activity_time(activity['start_time'],"iso") + 
                        "</div>" + 
                        "<div class='activity-location'>" + 
                            "Where: " + "<a href='/location/" + location['id'] + "' >" + location['name'] + "</a> - " + location['city'] + ", " + location['state'] + 
                        "</div>"
      								"</li>";
      		}
      		content = content + "</ul>";
      		$(el).html(content);
    	}
  	});
}

// Handle the follow function
// Status: Completed
function follow_callback(data) {
  $("#follow_handler").val("Unfollow");
  var location_id = $("#location_id").val();
  var member_follow_username = data['username']
  var member_follow_name = data['name']
  var member_follow_avatar = data['avatar']
  var s = "<li class='follower-item-data' id='member_" + member_follow_username + "' >" + 
              "<a href='/" + member_follow_username + "' rel='tooltip' title='" + member_follow_name + "' >" + 
                  "<img src=" + member_follow_avatar + " width=80 height=80 />" + 
              "</a>" + 
              "</li>"
  $('.follower-list-data').append(s)
}

// Handle the unfollow function
// Status: Completed
function unfollow_callback(data) {
  $("#follow_handler").val("Follow");
  var location_id = $("#location_id").val();
  var member_follow_username = data['username']
  $("#member_" + member_follow_username).remove()
}

function recommend_friend_callback(data) {
  $("#modal_friend").modal('hide');
  $('#modal_friend input[type=checkbox]').attr('checked', false);
  $('#send_recommend_btn').addClass('disabled')
  var s = '<p class="notice-message">Your recommendation has been sent to your friends</p>'
  var el = "#show_notice_message"
  show_message(s,el)
}

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
    var s = "<li class='comment-item-data' id='comment-" + data['comment_id'] + "' >" +
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
  Dajaxice.frittie.app.location.remove_comment(remove_comment_callback,{'comment_id': comment_id}, {'error_callback': custom_error})
}
// Report comment handle function. This is completed
function report_comment(comment_id) {
    var is_login = $("#check_login").val();
    var location_id = $("#location_id").val();
  if (is_login == "True"){
        Dajaxice.frittie.app.location.report_comment(report_comment_callback,{'comment_id': comment_id}, {'error_callback': custom_error})
    } else {
        window.location.href = WEBSITE_HOMEPAGE + "/login/?next=/location/" + location_id;
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
          Dajaxice.frittie.app.location.edit_comment(edit_comment_callback,
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
          if (el_error_exist) $(remove_el).remove()
      }
    return process
}


function addfrit_callback(data){
  if (data['current']== "You have already fritted !!")
      {
        var frittext = data['current']
        $('.frit-section').html(frittext)
      }
      else
      {
        var frittext = data['current'] + " fritties"
        $('.frit-section').html(frittext)
      }
}

function removefrit_callback(data){
    var frittext = data['current']
     $('.unfrit-section').html(frittext)
  }