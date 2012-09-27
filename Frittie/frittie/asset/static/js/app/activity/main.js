$(document).ready(function () {
	var is_login = $("#check_login").val();
  var activity_id = $("#activity_id").val();

  if ($('#page_type').val() == 'normal_page') {
      // Handle the comment action
      // Status: complete
	     $("#comment_box").keypress(function(e) {
        // Shift-Enter key action
          if (e.which == 13 && e.shiftKey) {
            var content = this.value;
            var caret = getCaret(this);
            this.value = content.substring(0,caret);
            e.stopPropagation();
          } 
        
          // Enter key action. Handle the comment here
          else if (e.which == 13) {
    		    var comment_content = $("#comment_box").val();
            if (strip_whitespace(comment_content).length != 0) {
       		     Dajaxice.frittie.app.activity.add_comment(add_comment_callback,
       						{'activity_id': activity_id,'comment_content': comment_content}, {'error_callback': custom_error})
            } else {
              return false;
            }
    	     }	
        });

      $("#join_handler").click(function() {
          if ($(this).val() == "Join"){
              if (is_login == "True"){
                  Dajaxice.frittie.app.activity.join_activity_request(join_activity_callback,{'activity_id': activity_id})
              } else {
                  window.location.href = WEBSITE_HOMEPAGE + "/login/?next=/activity/" + activity_id;
              }
          } else {
              $("#modal_cancel_attend").modal('show')
          }
      });

      $("#unjoin_handler").mouseover(function() {
          $("#unjoin_handler").popover('show')
      })  

      // _What it does: Allow user who create this location edit its info
      // _Purpose: Redirect to the edit location page
      // Status: Completed
      $("#edit_handler").click(function() {
          window.location.href = WEBSITE_HOMEPAGE + "/activity/" + activity_id + "/edit/";
      });

      $("#send_cancel_message_btn").click(function() {
          $("#modal_cancel_attend").modal("hide");
          var message = $('#cancel_message').val()
          Dajaxice.frittie.app.activity.cancel_joining_activity(cancel_joining_callback,{'activity_id': activity_id,'message':message})
      });

      // _What it does: Handle when user click on the recommend button
      // _Purpose: open the modal box include all friends for user to select
      // _Status: Completed
      $("#recommend_btn").click(function() {
          if (is_login == "True"){
            $('#modal_friend').modal('show')
          } else {
            window.location.href = WEBSITE_HOMEPAGE + "/login/?next=/activity/" + activity_id;
          }
      });

      $("#send_recommend_btn").click(function(){
          var friends = [];
          $('#modal_friend input[type=checkbox]:checked').each(function(index, value){ 
              var name =  $(this).attr("name");
              friends.push(parseInt(name.substring(7,name.length),10));      
          });
          Dajaxice.frittie.app.activity.recommend_friend(recommend_friend_callback,{'activity_id': activity_id,'friends': friends})
      });

      $("#upload_photo_btn").click(function() {
          if (is_login == "True"){
              Dajaxice.frittie.app.photo.upload_activity_photo(upload_activity_photo_callback,{'activity_id': activity_id})
          } else {
              window.location.href = WEBSITE_HOMEPAGE + "/login/?next=/activity/" + activity_id;
          }
      })

      $('#modal_upload_photo').on('hide',function() {
          console.log('yes')
          Dajaxice.frittie.app.photo.update_streams(update_streams_callback,{})
      })

  } else {
  
  }
})