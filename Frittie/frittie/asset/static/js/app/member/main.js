$(document).ready(function () {

  /**********************************
  *                                 *
  *     INITIAL AND GLOBAL DATA     *
  *                                 *
  **********************************/
  var is_login = $("#check_login").val();
  var member_view_username = $('#member_view_username').val()

  /*****************************************
  *                                        *
  *     INITIAL THE STAR RATING PLUGIN     *
  *                                        *
  *****************************************/
  $(".star-rating").raty({
      readOnly: true,
      half  : true,
      score: function() {
        return $(this).attr('data-rating');
    }
  })


  /**********************************
  *                                 *
  *     HANDLE NORMAL USER PAGE     *
  *                                 *
  **********************************/
  if ($('#page_type').val() == 'normal_page') {


      /**********************************
      *                                 *
      *     HANDLE TAB NAVIGATION       *
      *                                 *
      **********************************/
      $('#toolbar_tab a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
      })

      $('#activity_tab a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
      })

      $('#location_tab a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
      })

      /**************************************
      *                                     *
      *     HANDLE SEND MESSAGE FEATURE     *
      *                                     *
      **************************************/
	   $("#message_btn").click(function() {
        if (is_login == "True"){
          $('#modal_send_message').modal('show')
        } else {
          window.location.href = WEBSITE_HOMEPAGE + "/login/?next=/" + member_view_username;
        }
  	 });

     $("#send_message_btn").click(function() {
        var member_chat_username = $("#member_view_username").val();
        var message_content = $("#message_box").val()
        if (strip_whitespace(message_content).length != 0) {
            Dajaxice.frittie.app.message.add_message(add_message_callback,{'username': member_chat_username, 'message': message_content})
        } else {
          return false
        }
      });


    /**********************************
    *                                 *
    *     HANDLE ADMIN USER PAGE      *
    *                                 *
    **********************************/
  } else {
    
    /*********************************************************
    *                                                        *
    *     HANDLE AUTOCOMPLETE FOR CHOOSE LOCATION POP UP     *
    *                                                        *
    *********************************************************/
    var choose_location_autocomplete_data = []
    for (var i=0; i < autocomplete_data.length; i++) {
      if (autocomplete_data[i]['type'] == 'location') {
          choose_location_autocomplete_data.push(autocomplete_data[i])
      } 
    }
    choose_location_autocomplete(choose_location_autocomplete_data)

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

    /*****************************************************
    *                                                    *
    *     HANDLE CHOOSE LOCATION AND CREATE ACTIVITY     *
    *                                                    *
    *****************************************************/
    var age_range_from_el = "#create_activity_form input[name=activity_age_range_from]"
    var age_range_to_el = "#create_activity_form input[name=activity_age_range_to]"
    var limit_people = "#create_activity_form input[name=activity_limit]"
    var unlimited_people = '#create_activity_form input[name=activity_unlimited]'
    var location_type_el = '#modal_choose_location select[name=location_type]'
    var location_special_el = '#modal_choose_location select[name=location_special]'
    var zipcode_el = "#create_location_form input[name='location_zipcode']"

    $("#create_normal_activity_btn").click(function() {
        Dajaxice.frittie.app.location.load_location(load_location_callback,{'location_name':null,'location_type': 'All','location_special':'most_rated'})
    })

    $(location_type_el).change(function() {
        var location_type = $(this).val()
        var location_special = $(location_special_el).val()
        Dajaxice.frittie.app.location.load_location(load_location_callback,{'location_name':null,'location_type': location_type,'location_special':location_special})
    })

    $(location_special_el).change(function() {
        var location_type = $(location_type_el).val()
        var location_special = $(this).val()
        Dajaxice.frittie.app.location.load_location(load_location_callback,{'location_name':null, 'location_type': location_type,'location_special':location_special})
    })

    $('#modal_choose_location').on('hide',function(){
        $('#choose_location_id').val('')
        $('#search_location_query').val('')
        $('#choose_location_btn').addClass('disabled')
    })

    $("#choose_location_btn").click(function(){
        if ($(this).hasClass('disabled') == false) {
          var location_id = $('#choose_location_id').val()
          $('.activity-age-range-row').hide();
          $('.activity-limit-value').hide() 
          $(unlimited_people).attr('checked', true);

          $('#modal_choose_location').modal('hide')
          $('#modal_create_activity').modal('show')
          $('#choose_location_id').val(location_id)
        } else {
          return false;
        }
    })

    $('#back_to_choose_location_btn').click(function() {
        $('#modal_create_activity').modal('hide')
        $('#modal_choose_location').modal('show')
    })

    $("#search_location_query").change(function() {
        var location_name = $(this).val()
        var location_type = $(location_type_el).val()
        var location_special = $(location_special_el).val()
        Dajaxice.frittie.app.location.load_location(load_location_callback,{'location_name':location_name, 'location_type': location_type,'location_special':location_special})
    })

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
      var check_name = is_empty("#create_activity_form input[name='activity_name']")
      var check_starttime = is_empty("#create_activity_form input[name='activity_starttime']")
      var check_endtime = is_empty("#create_activity_form input[name='activity_endtime']")
      var name_error_exist = is_el_exist(".activity-name-row .data-error")
      var starttime_error_exist = is_el_exist(".activity-starttime-row .data-error")
      var endtime_error_exist = is_el_exist(".activity-endtime-row .data-error")
      var process = true
      if (check_name) {
          if (!name_error_exist) {
              $('.activity-name-row').append(s)
          }
          process = false
      } else {
          if (name_error_exist) $(".activity-name-row .data-error").remove()
      }
      if (check_starttime) {
          if (!starttime_error_exist) {
               $('.activity-starttime-row').append(s)
          } 
          process = false
      }  else {
           if (starttime_error_exist) $(".activity-starttime-row .data-error").remove()
      }

      if (check_endtime) {
          if (!endtime_error_exist) {
              $('.activity-endtime-row').append(s)
          }
          process = false
      }  else {
           if (endtime_error_exist) $(".activity-endtime-row .data-error").remove()
      }
      
      return process
    })
    
    $("#send_cancel_message_btn").click(function() {
          $("#modal_cancel_activity").modal("hide");
          var message = $('#cancel_message').val()
          var activity_id = parseInt($('#current_activity_action').val(),10)
          Dajaxice.frittie.app.activity.cancel_joining_activity(cancel_joining_callback,{'activity_id': activity_id,'message':message})
    });


    /*********************************
    *                                *
    *     HANDLE CREATE LOCATION     *
    *                                *
    **********************************/
    var zipcode_el = "#create_location_form input[name='location_zipcode']"

    $(function(){
      $(zipcode_el).data('val',  $(zipcode_el).val() ); 

      $(zipcode_el).change(function() { 
        is_numeric(this,'',{})
      });

      $(zipcode_el).focusout(function() {
        if( $(zipcode_el).val() != $(zipcode_el).data('val') ){ 
            $(zipcode_el).data('val',  $(zipcode_el).val() ); 
            $(this).change(); 
        }
      })

    });

    $('#init_create_location_btn').click(function() {
      $('#modal_create_location').modal('show')
    })

    $("#final_create_location_btn").click(function() {
      var s = "<td class='data-error'>" + 
                  "This field is required" + 
              "</td>"
      var invalid_name = is_empty("#create_location_form input[name='location_name']")
      var invalid_address1 = is_empty("#create_location_form input[name='location_address1']")
      var invalid_city = is_empty("#create_location_form input[name='location_city']")
      var invalid_zipcode = is_empty(zipcode_el)
      var name_error_exist = is_el_exist(".location-name-row .data-error")
      var address1_error_exist = is_el_exist(".location-address1-row .data-error")
      var city_error_exist = is_el_exist(".location-city-row .data-error")
      var zipcode_error_exist = is_el_exist(".location-zipcode-row .data-error")
      var process = true
      process = validate_field(invalid_name,name_error_exist,'.location-name-row','.data-error',process,s) 
      process = validate_field(invalid_address1,address1_error_exist,'.location-address1-row','.data-error',process,s) 
      process = validate_field(invalid_city,city_error_exist,'.location-city-row','.data-error',process,s) 
      process = validate_field(invalid_zipcode,zipcode_error_exist,'.location-zipcode-row','.data-error',process,s)
      console.log(process)
      return process
    })
  }
})