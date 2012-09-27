$(document).ready(function () {
	search_autocomplete(autocomplete_data);	

	// initialize scrollable
  	$(".slideshow").scrollable();

  	// Hide elements
  	$('#Header .nav-right .discover').hide()
	$('#create_things_modal').hide()
	$('.search-result').hide()
	$('.sidebar-section').hide()

	$('.user-account').hover(
		function() {
			$('.user-account').addClass('user-account-hover-effect')
			$('.user-menu').addClass('user-account-hover-effect')
		},
		function() {
			$('.user-account').removeClass('user-account-hover-effect')
			$('.user-menu').removeClass('user-account-hover-effect')
		}
	)

	$('.user-menu').hover(
		function() {
			$('.user-menu-area').addClass('open')
			$('.user-account').addClass('user-account-hover-effect')
			$('.user-menu').addClass('user-account-hover-effect')
		},
		function() {
			$('.user-menu-area').removeClass('open')
			$('.user-account').removeClass('user-account-hover-effect')
			$('.user-menu').removeClass('user-account-hover-effect')
		}
	)

	// This class prevent the tag <a> move user to
	// the top of the page when user click on that
	$('.disable-link-top').click(function(event) {
		event.preventDefault()
	}) 

	$('#handler_sidebar').click(function() {
        if ($('#sidebar_section_value').val() == "Open") {
            open_sidebar()
        } else {
            close_sidebar()
        }
        update_typeahead_width()
    }) 

})