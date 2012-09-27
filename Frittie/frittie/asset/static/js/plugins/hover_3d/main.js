$(document).ready(function () {

    $('#location_data li:nth-child(3n)').addClass('end-row');
    $('#location_data li:nth-child(3n+1)').addClass('first-row');
    
      // Load API resource to get the appropriate kind of location category
	   $(".category1").click(function(){
  		var url = WEBSITE_HOMEPAGE + "/api/frittie/location/?format=json&category=" + "Restaurant";
  		list_location(url)	
  	});
  	$(".category2").click(function(){
  		var url = WEBSITE_HOMEPAGE + "/api/frittie/location/?format=json&category=" + "Dating";
  		list_location(url)	
  	});
  	$(".category3").click(function(){
  		var url = WEBSITE_HOMEPAGE + "/api/frittie/location/?format=json&category=" + "Shopping";
  		list_location(url)	
  	});
  	$(".category4").click(function(){
  		var url = WEBSITE_HOMEPAGE + "/api/frittie/location/?format=json&category=" + "Movie";
  		list_location(url)	
  	});
  	$(".category5").click(function(){
  		var url = WEBSITE_HOMEPAGE + "/api/frittie/location/?format=json&category=" + "Camping";
  		list_location(url)	
  	});
  	$(".category6").click(function(){
  		var url = WEBSITE_HOMEPAGE + "/api/frittie/location/?format=json&category=" + "Entertaining";
  		list_location(url)	
  	});
})