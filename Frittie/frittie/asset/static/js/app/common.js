// Return default avatar if user dont have any avatar
function handle_user_avatar(avatar,gender) {
	if (avatar == null) 
		if (gender == "Male")
			return WEBSITE_HOMEPAGE + "/static/img/male_icon.gif"
		else
			return WEBSITE_HOMEPAGE + "/static/img/female_icon.gif"
	return avatar
}

// Return appropriate activity time from datetime string taken from API
function handle_activity_time(date,time_mode) {
	var activity_date;
	if (time_mode == "iso") {
		activity_date = iso_date_analyze(date)
	} else {
		activity_date = rfc_date_analyze(date)
	}
	var month = activity_date['month']
	var day = activity_date['day']
	return convert_24hr_to_AM_PM(month,day,activity_date['hour'],activity_date['minute']);
}

// Autocomplete function for the searching
function search_autocomplete(data_src) {
    var data = new Array(); 
    for (var i = 0; i < data_src.length; i++) {
        var dt = new Object();
        dt.label = data_src[i]['name']
        dt.value = data_src[i]['value']
        dt.description = data_src[i]['description']
        dt.icon = data_src[i]['icon']
        data.push(dt)
    }
    
    $("#search_query").autocomplete({
        source: data,
        minLength: 1,
        focus: function( event, ui ) {
            $( "#search_query" ).val( ui.item.label );
            return false;
        },
        select: function( event, ui ) {
          $( "#search_query" ).val( ui.item.label );
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

function get_age(user_year) {
    var date = new Date()
    var current_year = parseInt(date.getFullYear(),10);
    return (current_year - parseInt(user_year,10)).toString() + ' years old'
}

function get_gender(gender,possession) {
    var male = 'him'; 
    var female = 'her';
    if (possession) {
        male = "his"
    }
    if (gender == 'Female') {
        return female
    } else {
        return male
    }
}

function update_notify(data) {
    //console.log(data['new_notify'])
    if ($('#check_login').val() == "True") {
        if ((data['new_notify'] != '0') && ($('#member_login_username').val() == data['username'])) {
            console.log('yes')
            var s = "<a href='#user_menu' class='dropdown-toggle btn-mini' data-toggle='dropdown' >" + data['new_notify'] + "</a>";
            var new_item = $(s).hide();
            $('#new_notify').html(new_item);
            new_item.slideDown();
        }
        if ((data['new_buzz_type'] != '0') && ($('#member_login_username').val() == data['username'])) {
            console.log('yes1')
            var s =  "<a href='/buzz'>Buzz (" + data['new_buzz_type'] + ") </a>"
            $('#buzz').html(s);
        }
        if ((data['new_mail_type'] != '0') && ($('#member_login_username').val() == data['username'])) {
            console.log('yes2')
            var s =  "<a href='/messages'>Messages (" + data['new_mail_type'] + ") </a>"
            $('#messages').html(s);
        }
    }
}

function get_multiple_checkbox(el){
    var result = [];
    $(el).each(function(index, value){  
        var name =  $(this).attr("name");
        result.push(parseInt(name.substring(7,name.length),10));     
    });
    return result
}

// Update the typeahead area width to fit with the search bar
function update_typeahead_width() {
    var search_width = $('#search_query').width()
    $('.typeahead').width(search_width)
}

// Handle the search bar width when user resize the browser
function check_search_bar() {
    var main_body_width = $('#main_body').width()
    $('.brand-name').show()
    if ((main_body_width < 1200) && (main_body_width > 1100)) {
        $('#search_query').width(280)
    } else if ((main_body_width < 1100) && (main_body_width > 1000)) {
        $('#search_query').width(250)
    } else if (main_body_width < 1000) {
        $('#search_query').width(220)
    } else if (main_body_width > 1200) {
            $('#search_query').width(399)
    }
        update_typeahead_width()
}

function check_search_bar_responsive() {
    var main_body_width = $('#main_body').width()
    $('.brand-name').show()
    if ((main_body_width < 960) && (main_body_width > 850)) {
        $('#search_query').width(350)
    } else if ((main_body_width < 850) && (main_body_width > 750)) {
        $('#search_query').width(290)
    } else if ((main_body_width < 750) && (main_body_width > 650)) {
        $('#search_query').width(230)
    } else if (main_body_width < 650) {
        $('#search_query').width(230)
        $('.brand-name').hide()
    }
    update_typeahead_width()
}

function close_sidebar() {
      // Change some value when the connection is pop out
      $('#sidebar_section_value').val('Open')

      // Handle the search bar
      if( $('.navbar-search').is(":hidden") ) {
          $('.navbar-search').show()
      } 
      $('#search_query').width(280)

      // Handle the animation
      $('.discover').hide(200, function() {
          $(this).animate({
              width: 0,
          }, 200)
        }
      )
          
      $('.sidebar-section').hide(100, function() {
          $(this).animate({
            width: 0,
          }, 200)
        }
      )
      $('.main-section').css('width','100%')  
}

function open_sidebar() {

      // Change some value when the connection is pop out
      $('#sidebar_section_value').val('Close')

      // Handle the search bar when size is not enough
      var main_body_width = $('#main_body').width()
      var search_width = $('#search_query').width()
      if (main_body_width >  1300) { 
          $('#search_query').width(search_width-100)    
      } else if ((main_body_width < 1300) && (main_body_width > 1200)) {
          if (search_width > 199) {     
              $('#search_query').width(search_width-100)
          } else {
              $('#search_query').width(search_width-50)
          }
      } else if (main_body_width < 1200) {
          $('.navbar-search').hide()
      }

      // Handle the animation
      $('.main-section').width(main_body_width-340)    
      $('.discover').show(200, function() {
          $(this).animate({
              width: 243,
          }, 200)
        }
      )  

      $('.sidebar-section').show(200, function() {
          $(this).animate({
              width: 300,
          }, 200)
        }
      )
}



/*function open_responsive_area() {
    $('.responsive-icon').addClass('responsive-icon-effect')
    $('#Header').css('height','150px')
    $('#Header .container').css('height','148px')
    $('#Header .navbar-inner').css({
        'height': '148px',
        'background': 'url(http://db0dp9rjtl3zs.cloudfront.net/zaahah.com/v3/img/app/header/responsive-header-background.png) repeat-x'
    })

    var new_responsive_row = "<div class='responsive-row row-fluid' style='height: 100px'><ul></ul></div>"
    $('#Header .container').append(new_responsive_row)

    $('.responsive-element').detach().appendTo('.navbar-inner .responsive-row ul')
    $('.responsive-element').css({'position':'absolute','top': '50px','left':'20px'})
    var responsive_elements = $('.responsive-element')
    for (var i = 0; i < responsive_elements.length; i++) {
        var margin_top_val = (i + 1) * 20 + i * 14
        $(responsive_elements[i]).css('margin-top',margin_top_val)
    }
    $('.responsive-element').show()
}

function close_responsive_area() {
    $('.responsive-icon').removeClass('responsive-icon-effect')
    $('#Header').css('height','50px')
    $('#Header .container').css('height','48px')
    $('#Header .navbar-inner').css({
        'height': '48px',
        'background': 'url(http://db0dp9rjtl3zs.cloudfront.net/zaahah.com/v3/img/app/header/header-background-copy.png) repeat-x'
    })

    $('.responsive-element').hide()
    $('.responsive-element').css({'position':'relative','top': '0px','left':'0px','margin-top': '0px'})
    var responsive_elements = $('.responsive-element')
    for (var i = 0; i < responsive_elements.length; i++) {
        if ($(responsive_elements[i]).hasClass('left-element')) {
            var pivot_el = '.navbar-inner .normal-row .nav-left .responsive-pivot-' + i.toString()
            $(responsive_elements[i]).detach().insertAfter(pivot_el)
        } else {
            var pivot_el = '.navbar-inner .normal-row .nav-right .responsive-pivot-' + i.toString()
            $(responsive_elements[i]).detach().insertBefore(pivot_el)
        }
    }
    $('.navbar-inner .responsive-row').remove()
}

function responsive_top_bar() {
    if ( $('#check_responsive').val() == 'False') {
        $('.navbar-inner .nav-left .brand-name').css('margin-left','20px')
        $('.navbar-inner .responsive-hide').hide()
        $('.navbar-inner .nav-left li.search').detach().prependTo('.navbar-inner .nav-right')
        $('#search_query').css('margin-right','-10px')
        $('#Header form.search-bar .search-result').css('right','167px')
        $('#search_query').hide()
        $('#search_submit_btn').hide()
        $('.navbar-inner .responsive-show').show()
    }
    $('#check_responsive').val('True')
}

function normal_top_bar() {
    if ( $('#check_responsive').val() == 'True') {
        close_responsive_area()
        $('.navbar-inner .nav-left .brand-name').css('margin-left','45px')
        $('#responsive_search_btn').attr('src','http://db0dp9rjtl3zs.cloudfront.net/zaahah.com/v3/img/app/header/responsive-search-icon.png')
        $('#responsive_search_btn').css({'margin-top':'0px','left':'-20px'})
        $('.navbar-inner .responsive-show').hide()
        $('.navbar-inner .responsive-hide').show()
        $('.navbar-inner .nav-right li.search').detach().appendTo('.navbar-inner .nav-left')
        $('#search_query').css('margin-right','0px')
        $('#Header form.search-bar .search-result').css('right','57px')
        $('#search_query').show()
        $('#search_submit_btn').show()
    }
    $('#check_responsive').val('False')
}
*/
