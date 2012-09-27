// Autocomplete function for the searching
function friends_search_autocomplete(data_src,el) {
    var friends = new Array(); 
    for (var i = 0; i < data_src.length; i++) {
        var friend = new Object();
        friend.label = data_src[i]['name']
        friend.value = data_src[i]['value']
        friend.description = data_src[i]['description']
        friend.icon = data_src[i]['icon']
        friends.push(friend)
    }
    
    $(el).autocomplete({
        source: friends,
        minLength: 1,
        focus: function( event, ui ) {
            $(el).val( ui.item.label );
            return false;
        },
        select: function( event, ui ) {
            $(el).val( ui.item.label );
            window.location.href = "/messages/" + ui.item.value + "/#chat_box"
            return false;
        }
    })
    .data( "autocomplete" )._renderItem = function( ul, item ) {
        console.log(item.description)
        var inner_html = "<a>" +  
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

function add_message_callback(data) {

}

function update_messages(data) {
    var latest_message_el = $('ul.message-list-data li:first')
    var latest_message_id = latest_message_el.attr('id')
    var member_send_username = data['member_send_username']
    var member_send_avatar = data['member_send_avatar']
    var member_send_name = data['member_send_name']
    var msg_content = data['msg_content']
    var date = data['date']
    if ("message_from_" + member_send_username == latest_message_id) {
        latest_message_el.find('.message-content').html(msg_content)
        latest_message_el.find('.message-date').html('<p><small>' + date + "</small></p>")
    } else {
        var item_id = "#message_from_" + member_send_username
        if ($(item_id).length > 0) {
            $(item_id).parent().prepend($(item_id));
            $(item_id).find('.message-content').html(msg_content)
            $(item_id).find('.message-date').html('<p><small>' + date + "</small></p>")
        } else {
            var s = "<li class='message-item-data' id='message_from_" + member_send_username + "' >" + 
                                "<a href='/messages/" + member_send_username + "' >" + 
                                    "<div class='message-member'>" + 
                                        "<p>" +
                                            "<div class='message-member-avatar'>" +
                                                "<img src=" + member_send_avatar + " width=25 height=25>" +  
                                            "</div>" +
                                            "<div class='message-member-name'>" +
                                                "<h4>" +
                                                    member_send_name +
                                                "</h4>" +
                                            "</div>" +
                                        "</p>" +
                                    "</div>" +
                                    "<div class='message-content'>" +
                                        "<p>" +
                                            msg_content + 
                                        "</p>" +
                                    "</div>" + 
                                    "<div class='message-date'>" + 
                                        "<p><small>" + date + "</small></p>" +
                                    "</div>" +
                                "</a>" +
                                "<hr>" + 
                            "</li>"
            $('.message-list-data').prepend(s)
        }
    }
}


function chat(data) {
    var member_send_username = data['member_send_username']
    var member_send_avatar = data['member_send_avatar']
    var member_send_name = data['member_send_name']
    var msg_content = data['msg_content']
    var date = data['date']
    console.log()
    if (($('#member_chat_username').val() == member_send_username) || ($('#member_login_username').val() == member_send_username)){
        console.log('yes')
        var s = "<li class='message-item-data' >" + 
                "<div class='message-member'>" + 
                    "<p>" +
                        "<a href='/" + member_send_username + "' >" +
                            "<div class='message-member-avatar'>" +
                                "<img src=" + member_send_avatar + " width=25 height=25>" +  
                            "</div>" +
                            "<div class='message-member-name'>" +
                                "<h4>" +
                                    member_send_name +
                                "</h4>" +
                            "</div>" +
                        "</a>" + 
                    "</p>" +
                "</div>" +
                "<div class='message-content'>" +
                    "<p>" +
                        msg_content + 
                    "</p>" +
                "</div>" + 
                "<div class='message-date'>" + 
                    "<p><small>" + date + "</small></p>" +
                "</div>" +
                "<hr>" + 
            "</li>"
        if ($('#no_message_notice').length > 0) {
            var new_el = "<div id='message_main_display'>" + 
                        "<ul class='message-list-data'>" + 
                            s + 
                        "</ul>" + 
                    "</div>"
            $('#no_message_notice').remove()
            $('#message_area').prepend(new_el)
        } else {
            $('.message-list-data').append(s)
        }
        $("#chat_box").val('')
    } else {
        console.log('no')
    }
}
