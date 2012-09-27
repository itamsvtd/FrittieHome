$(document).ready(function () {
  
  /**********************************
  *                                 *
  *     INITIAL AND GLOBAL DATA     *
  *                                 *
  **********************************/
  var is_login = $("#check_login").val();
  var location_id = $("#location_id").val();
  var age_range_from_el = "#create_activity_form input[name=activity_age_range_from]"
  var age_range_to_el = "#create_activity_form input[name=activity_age_range_to]"
  var limit_people = "#create_activity_form input[name=activity_limit]"
  var unlimited_people = '#create_activity_form input[name=activity_unlimited]'
  $('.carousel').carousel();
  $(function() {
    $("#datepicker").datepicker();
  });


  /**************************************************************
  *                                                             *
  *     HANDLE START TIME - END TIME IN CREATE ACTIVITY FORM    *
  *                                                             *
  **************************************************************/
  $('#activity_starttime').datetimepicker({
      ampm: true,
      minDate: new Date(),
      onClose: function(dateText, inst) {
        var endDateTextBox = $('#activity_endtime');
        if (endDateTextBox.val() != '') {
            var testStartDate = new Date(dateText);
            var testEndDate = new Date(endDateTextBox.val());
            if (testStartDate > testEndDate)
                endDateTextBox.val(dateText);
        }
        else {
            endDateTextBox.val(dateText);
        }
    },
    onSelect: function (selectedDateTime){
        var start = $(this).datetimepicker('getDate');
        console.log(start.getTime())
        $('#activity_endtime').datetimepicker('option', 'minDate', new Date(start.getTime()) );
    }

  })
  $("#activity_endtime").datetimepicker({
      ampm: true,
      minDate: new Date(),
      onClose: function(dateText, inst) {
        var startDateTextBox = $('#activity_starttime');
        if (startDateTextBox.val() != '') {
            var testStartDate = new Date(startDateTextBox.val());
            var testEndDate = new Date(dateText);
            if (testStartDate > testEndDate)
                startDateTextBox.val(dateText);
        }
        else {
            startDateTextBox.val(dateText);
        }
      },
      onSelect: function (selectedDateTime){
        var end = $(this).datetimepicker('getDate');
        $('#activity_starttime').datetimepicker('option', 'maxDate', new Date(end.getTime()) );
      }         
  })


  /************************************
  *                                   *
  *     HANDLE FOLLOW LOCATION        *
  *                                   *
  ************************************/
  // _What it does: Handle the follow button
  // _Purpose: use dajaxice to communicate with server, add or remove user from follow_by 
  // property of this location and then return the new list of follower
  // _Status: completed
  $("#follow_handler").click(function() {
    if ($(this).val() == "Follow"){
      if (is_login == "True"){
          Dajaxice.frittie.app.location.follow_location(follow_callback,{'location_id': location_id})
      } else {
        window.location.href = WEBSITE_HOMEPAGE + "/login/?next=/location/" + location_id;
      }
    } else {
        Dajaxice.frittie.app.location.unfollow_location(unfollow_callback,{'location_id': location_id})
    }
  });


  /*******************************************
  *                                          *
  *     HANDLE RECOMMEND FRIEND FEATURE      *
  *                                          *
  *******************************************/
  // _What it does: Handle when user click on the recommend button
  // _Purpose: open the modal box include all friends for user to select
  // _Status: Completed
  $('#modal_friend input[type=checkbox]').change(function() {
      var el = '#modal_friend input[type=checkbox]:checked'
      friends = get_multiple_checkbox(el)
      console.log(friends.length)
      if (friends.length == 0) {
        $('#send_recommend_btn').addClass('disabled')
      } else {
        $('#send_recommend_btn').removeClass('disabled')
      }
  }) 

  $("#recommend_btn").click(function() {
      if (is_login == "True"){
        $('#modal_friend').modal('show')
      } else {
        window.location.href = WEBSITE_HOMEPAGE + "/login/?next=/location/" + location_id;
      }
    });

  // _What it does: Handle the recommend friend process
  // _Purpose: Check how many friend user select, not allow user to proceed if he/she select
  // nobody. Use the same ajax technique (dajaxice) to communicate with server, handle the
  // process over there and return the message notify the action has been done
  // _Status: Not completed
  $("#send_recommend_btn").click(function(){
      var el = '#modal_friend input[type=checkbox]:checked'
      friends = get_multiple_checkbox(el)
      if (friends.length != 0) {
          Dajaxice.frittie.app.location.recommend_friend(recommend_friend_callback,{'location_id': location_id,'friends': friends})
      }
  });


  /****************************************
  *                                       *
  *     HANDLE EDIT LOCATION FEATURE      *
  *                                       *
  ****************************************/
  // _What it does: Allow user who create this location edit its info
  // _Purpose: Redirect to the edit location page
  // Status: Completed
  $("#edit_btn").click(function() {
      window.location.href = WEBSITE_HOMEPAGE + "/location/" + location_id + "/edit/";
  });


  /**************************************************
  *                                                 *
  *     HANDLE FILTER ACTIVITY BY DATE FEATURE      *
  *                                                 *
  **************************************************/
	$('#datepicker').datepicker({
    	onSelect: function(dateText, inst) {
    		var select_year = dateText.substring(6);
    		var select_month = dateText.substring(0,2);
    		var select_day = dateText.substring(3,5);   		
        var query = select_year + "-" + select_month + "-" + select_day;
        var url = WEBSITE_HOMEPAGE + "/api/frittie/activity/?format=json&start_time__gte=" + query;
        var el = ".location-activity";
        list_activity(url,el);
    	}
	});

  /***********************************
  *                                  *
  *     HANDLE COMMENTING FEATURE    *
  *                                  *
  ***********************************/
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
              Dajaxice.frittie.app.location.add_comment(add_comment_callback,
                  {'location_id': location_id,'comment_content': comment_content}, {'error_callback': custom_error})
          } else {
            return false;
        }
      } 
  });


  /*************************************
  *                                    *
  *     HANDLE firtnumber*
  *                                    *
  *************************************/
  // _What it does: Frit and Unfrit a location
  // _Purpose: Open create the frit
  // _Status: Complete
  $("#fritlocation").click(function(){
    if (is_login == "True"){
        Dajaxice.frittie.app.location.addfritlocationnumber(addfrit_callback,{'location_id': location_id})
      }
      
  });

  $("#unfritlocation").click(function(){
    if (is_login == "True"){
        Dajaxice.frittie.app.location.removefritlocationnumber(removefrit_callback,{'location_id': location_id})
      }
      
  });
  /*************************************
  *                                    *
  *     HANDLE CREATE ACTIVITY FORM    *
  *                                    *
  *************************************/
  // _What it does: Handle the create activity process
  // _Purpose: Open the modal create activity
  // _Status: Complete
  $("#init_create_activity_btn").click(function(){
      if (is_login == "True"){
        $('.activity-age-range-row').hide();
        $('.activity-limit-value').hide() 
        $(unlimited_people).attr('checked', true);
        $('#modal_create_activity').modal('show')
      } else {
        window.location.href = WEBSITE_HOMEPAGE + "/login/?next=/location/" + location_id;
      }
      
  });

  $('#create_activity_form input[name=activity_unlimited]').click(function() {
        if ($(unlimited_people).attr('checked')) {
            $('.activity-limit-value').hide()
        } else {
            $('.activity-limit-value').show()
        }
  })

  $("select[name='activity_type']").change(function(){
      var type_description = ""
      $("select[name='activity_type'] option:selected").each(function() {
          if ($(this).val() == 'blind_date') {
              type_description = 'Blind date activity is for everyone looking for their soulmate.'
              $('.activity-age-range-row').show()
              $('.activity-limit-row').hide()
          } else {
              $('.activity-age-range-row').hide()
              $('.activity-limit-row').show()
          }
          if ($(this).val() == 'invite_only') {
            type_description = 'Invite only activity is open to who get the invitation. Other people cannot see or find this activity'
          } 
          if ($(this).val() == 'anonymous') {
            type_description = 'Anonymous activity is open to everyone but their info will be hidden. Nobody know who will join the activity '
          } 
          if ($(this).val() == 'public') {
            type_description = 'Public activity is open to everyone. All people join in this will be displayed their info'
          }
      })
      $(".activity-type-description").html(type_description)
  }) 

  $('#modal_create_activity').on('hide', function ()  {
      $("select[name='activity_type'] option[value='public']").attr('selected','selected')
      if ($(".activity-age-range-row").length > 0){
        $('.activity-age-range-row').hide()
      }
      var s = "Public activity is open to everyone. All people join in this will be displayed their info"
      $('.activity-type-description').html(s)   
      $(unlimited_people).attr('checked', true);
      $('.activity-limit-row').show()
      $('.activity-limit-value').hide() 
  })

  $(function(){
    $(age_range_from_el).data('val',  $(age_range_from_el).val() ); // save value
    $(age_range_to_el).data('val',  $(age_range_to_el).val() ); // save value
    $(limit_people).data('val',  $(limit_people).val() ); // save value

    $(age_range_from_el).change(function() { 
        is_numeric(this,18,{'min':18,'max':99})
        compare_age(this,age_range_to_el)
    });

    $(age_range_to_el).change(function() { 
        is_numeric(this,30,{'min':19,'max':99})
        compare_age(age_range_from_el,this)
    })

    $(limit_people).change(function() { 
        is_numeric(this,10,{})
    })

    $(age_range_from_el).focusout(function() { 
        if( $(age_range_from_el).val() != $(age_range_from_el).data('val') ){ 
            $(age_range_from_el).data('val',  $(age_range_from_el).val() );
            $(this).change();
        }
    });

    $(age_range_to_el).focusout(function() { 
        if( $(age_range_to_el).val() != $(age_range_to_el).data('val') ){ 
            $(age_range_to_el).data('val',  $(age_range_to_el).val() ); 
            $(this).change(); 
        }
    });

    $(limit_people).focusout(function() {
        if( $(limit_people).val() != $(limit_people).data('val') ){ 
            $(limit_people).data('val',  $(limit_people).val() ); 
            $(this).change(); 
        }
    })

  });

  $("#final_create_activity_btn").click(function() {
      var s = "<td class='data-error'>" + 
                  "This field is required" + 
              "</td>"
      var invalid_name = is_empty("#create_activity_form input[name='activity_name']")
      var invalid_starttime = is_empty("#create_activity_form input[name='activity_starttime']")
      var invalid_endtime = is_empty("#create_activity_form input[name='activity_endtime']")
      var name_error_exist = is_el_exist(".activity-name-row .data-error")
      var starttime_error_exist = is_el_exist(".activity-starttime-row .data-error")
      var endtime_error_exist = is_el_exist(".activity-endtime-row .data-error")
      var process = true
      process = validate_field(invalid_name,name_error_exist,'.activity-name-row','.data-error',process,s)
      process = validate_field(invalid_starttime,starttime_error_exist,'.activity-starttime-row','.data-error',process,s)
      process = validate_field(invalid_endtime,endtime_error_exist,'.activity-endtime-row','.data-error',process,s)               
      return process
  })

  $("#update_location_handler").click(function() {
      var location_name_el = "#location_header .title"
      var location_description_el = "#location_description .description"
      var location_category_el = '#location_basic_info .category'
      var location_address1_el = '#location_basic_info .location-address1'
      var location_address2_el = '#location_basic_info .location-address2'
      var location_city_el = '#location_basic_info .location-city'
      var location_state_el = '#location_basic_info .location-state'
      var location_zipcode_el = '#location_basic_info .location-zipcode'
      var location_preference_el = '#location_preference'
      if ($(this).val() == 'Edit') {

      }
      else if ($(this).val() == 'Update') {

      }
  })
})