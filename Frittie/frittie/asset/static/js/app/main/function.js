function list_location(url) {
	$.ajax({
    	url:url,
    	type:"GET",
    	accepts:"application/json",
    	dataType:"json",
    	success:function(data){
      		var content = "<ul id='location_data'>";
      		for (var i = 0; i < data['objects'].length; i++)
      		{
      			var location = data['objects'][i];
      			content = content + "<li>" + 
      									"<div class='location-name'><a href='/location/" + location['id'] + "' >" + location['name'] + "</a></div>" +
      									"<div class='location-avatar'><a href='/location/" + location['id'] + "' ><img src=" + location['avatar'] + " width=150 height=175/></a></div>" + 
      									"<div class='location-address'>" + location['city'] + ", " + location['state'] + "</div>" +
      								"</li>";
      		}
      		content = content + "</ul>";
      		$("#location_area").html(content);
    	}
  	});
}


function list_activity(url) {
	$.ajax({
    	url:url,
    	type:"GET",
    	accepts:"application/json",
    	dataType:"json",
    	success:function(data){
    		var content = "<ul id='activity_data'>";
      		for (var i = 0; i < data['objects'].length; i++)
      		{
      			var activity = data['objects'][i];      		
            var member_create = activity['member_create'];	
            var user_create = member_create['user'];
            var location = activity['location'];
      			content = content + "<li>" + 
      									"<div class='activity-name'>" + 
                            "<a href='/activity/" + activity['id'] + "' >" + activity['name'] + "</a>" + 
                        "</div>" +                        
      									"<div class='activity-user-create pull-right'><a href='/" + user_create['username'] + "' >" + 
                                  "<img src=" + handle_user_avatar(member_create['avatar']) + " width=40 height=40 />" + 
                                  user_create['first_name'] + " " + user_create['last_name'] + "</a>" + 
                        "</div>" + 
                        "<div class='activity-time'>" + 
                            "When: " + handle_today_activity_time(activity['start_time'],"iso") + 
                        "</div>" + 
                        "<div class='activity-location'>" + 
                            "Where: " + "<a href='/location/" + location['id'] + "' >" + location['name'] + "</a> - " + location['city'] + ", " + location['state'] + 
                        "</div>"
      								"</li>";
      		}
      		content = content + "</ul>";
      		$("#activity_area").html(content);
    	}
  	});
}