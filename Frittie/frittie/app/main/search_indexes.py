from haystack.indexes import *
from haystack import site
from frittie.app.main.models import Location, Member, Activity

class LocationIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    create_by = CharField(model_attr='create_by')
    zip_code = CharField(model_attr='zip_code')
    followe_by = CharField(model_attr='follow_by')
    state = CharField(model_attr='state')
    city = CharField(model_attr='city')
   
class ActivityIndex(SearchIndex):
	text = CharField(document=True, use_template=True)
	member_create = CharField(model_attr='member_create')
	member_join = CharField(model_attr='member_join')
	start_time = DateTimeField(model_attr='start_time')
	end_time = 	DateTimeField(model_attr='end_time')

class MemberIndex(SearchIndex):
	text = CharField(document=True, use_template=True)
	user = CharField(model_attr='user')

site.register(Location, LocationIndex)
site.register(Member, MemberIndex)
site.register(Activity, ActivityIndex)