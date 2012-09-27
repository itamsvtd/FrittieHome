from django.shortcuts import render_to_response
from frittie.helper.common_helper import get_member_login_object, get_autocomplete_data
from django.template import RequestContext, Context, loader

def about_us(request):
	autocomplete_data = get_autocomplete_data(request)
	member_login = get_member_login_object(request)
    	return render_to_response("info_template/page/about_us.html",
    				{
                		"member_login": member_login,
                		'autocomplete_data': autocomplete_data,
            		},
            		context_instance = RequestContext(request)
    			)
    
def career(request):
	autocomplete_data = get_autocomplete_data(request)
	member_login = get_member_login_object(request)
    	return render_to_response("info_template/page/career.html",
					{
                		"member_login": member_login,
                		'autocomplete_data': autocomplete_data,
            		},
            		context_instance = RequestContext(request)
    			)

def contact_us(request):
	autocomplete_data = get_autocomplete_data(request)
	member_login = get_member_login_object(request)
    	return render_to_response("info_template/page/contact_us.html",
    				{
                		"member_login": member_login,
                		'autocomplete_data': autocomplete_data,
            		},
            		context_instance = RequestContext(request)
    			)
    
def copyright(request):
	autocomplete_data = get_autocomplete_data(request)
	member_login = get_member_login_object(request)
    	return render_to_response("info_template/page/copyright_trademark.html",
    				{
                		"member_login": member_login,
                		'autocomplete_data': autocomplete_data,
            		},
            		context_instance = RequestContext(request)
    			)
    
def help_page(request):
	autocomplete_data = get_autocomplete_data(request)
	member_login = get_member_login_object(request)
    	return render_to_response("info_template/page/help.html",
					{
                		"member_login": member_login,
                		'autocomplete_data': autocomplete_data,
            		},
            		context_instance = RequestContext(request)
    			)
    
def privacy_policy(request):
	autocomplete_data = get_autocomplete_data(request)
	member_login = get_member_login_object(request)
    	return render_to_response("info_template/page/privacy_policy.html",
					{
                		"member_login": member_login,
                		'autocomplete_data': autocomplete_data,
            		},
            		context_instance = RequestContext(request)
    			)
    
def team(request):
	autocomplete_data = get_autocomplete_data(request)
	member_login = get_member_login_object(request)
    	return render_to_response("info_template/page/team.html",
    				{
                		"member_login": member_login,
                		'autocomplete_data': autocomplete_data,
            		},
            		context_instance = RequestContext(request)
    			)
    
def term_service(request):
	autocomplete_data = get_autocomplete_data(request)
	member_login = get_member_login_object(request)
    	return render_to_response("info_template/page/term_service.html",
    				{
                		"member_login": member_login,
                		'autocomplete_data': autocomplete_data,
            		},
            		context_instance = RequestContext(request)
    			)
            
def safety(request):
	autocomplete_data = get_autocomplete_data(request)
	member_login = get_member_login_object(request)
    	return render_to_response("info_template/page/safety.html",
    				{
                		"member_login": member_login,
                		'autocomplete_data': autocomplete_data,
            		},
            		context_instance = RequestContext(request)
    			)
