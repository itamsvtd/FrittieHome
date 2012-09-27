# SESSION_KEY is used to defined if user login or not
SESSION_KEY = '_auth_user_id'

# since the url of member is www.frittie.com/username -> we need to 
# prevent user to enter username like login/logout since this will
# conflict with www.frittie.com/login and www.frittie.com/logout 
KEYWORD_URL = [
				'admin','signup','login','password',
				'logout','confirm_email','search','settings',
				'buzz','messages','location','activity',
				'info','api','asset','photo','feeds','friends'
			  ]

#######################################################
#								  					  #
#	These field is used to retrieve JSON format	      #
#	in 2 function: get_JSON_exclude_field and 		  #
#	get_JSON_include_field							  #
#													  #
#######################################################

# User Constant Setting
USER_COMMON_INCLUDE_FIELDS = [
			"username",
			"first_name",
			"last_name",
		]

# Member Constant Setting
MEMBER_USER_RELATIONS = {
			'user' : {
				'fields': ['username','first_name','last_name']
			}
		}


# Activity Constant Setting
ACTIVITY_TODAY_FEEDS_RELATIONS = [
		{
			'member_create': {
				'relations': { 
					'user': { 
						'fields': ['first_name','last_name']
					}
				}
			}
		},
		{
			'location': {
				'fields':['name','city','state','country']
				}
		}
	]


