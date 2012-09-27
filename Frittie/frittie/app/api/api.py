from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from frittie.app.main.models import Member, Location, Activity, Comment
from frittie.app.api.authentication import CustomAuthentication
from django.db.models import Q
from friends.models import Friendship
from frittie.helper.settings_helper import SESSION_KEY
from frittie.helper.activity_helper import get_today_activity
from frittie.app.api.serializer import PrettyJSONSerializer

# # List current login user, current viewing user
# # and all of his/her friends
# class UserResource(ModelResource):
#     class Meta:
#         queryset = User.objects.all()
#         resource_name = 'user'
#         fields = ['username', 'first_name', 'last_name']
#         filtering = {
#            "username": ("exact",),
#            "email": ("exact",),
#         }
#         include_resource_uri = False
#         serializer = PrettyJSONSerializer()
#         authentication = Authentication()
#         authorization = DjangoAuthorization()

#     def get_object_list(self, request): 
#         friends = []
#         current_username = None
#         login_username = None
#         if "current_user" in request.session:
#             current_username = request.session['current_user']
#             user = User.objects.get(username=current_username)
#             friends = Friendship.objects.friends_of(user).values_list('id', flat=True)
#         if SESSION_KEY in request.session:
#             login_username = User.objects.get(pk=request.session[SESSION_KEY]).username
#         return super(UserResource, self).get_object_list(request).filter(
#                 Q(username=current_username) | Q(pk__in=friends) | Q(username=login_username)
#             )

# # Extend member class of the user resource above
# class MemberResource(ModelResource):
#     user = fields.ForeignKey(UserResource, 'user', full=True)

#     class Meta:
#         queryset = Member.objects.all()
#         resource_name = 'member'
#         filtering= {
#             "user": ALL_WITH_RELATIONS,
#         }
#         serializer = PrettyJSONSerializer()
#         include_resource_uri = False
#         authentication = Authentication()
#         authorization = DjangoAuthorization()

#     def get_object_list(self, request):    
#         friends = []
#         current_user= None
#         login_user = None
#         if "current_user" in request.session:
#             current_user = User.objects.get(username=request.session['current_user'])
#             friends = Friendship.objects.friends_of(current_user).values_list('id', flat=True)
#         if SESSION_KEY in request.session:
#             login_user = User.objects.get(pk=request.session[SESSION_KEY])
#         return super(MemberResource, self).get_object_list(request).filter(
#                 Q(user=current_user) | Q(user__pk__in=friends) | Q(user=login_user)
#            )
#
# class LocationResource(ModelResource):
#     create_by = fields.ForeignKey(MemberResource, 'create_by', full=True)
#     follow_by = fields.ToManyField(MemberResource, 'follow_by', full=True)
#     class Meta:
#         queryset = Location.objects.all()
#         resource_name = 'location'
#         filtering = {
#             "create_by": ALL_WITH_RELATIONS,
#             "follow_by": ALL_WITH_RELATIONS,
#             "name": ("exact",),
#             "category": ("exact",),
#             "special": ("exact"),
#             "id": ("exact",),
#         }
#         serializer = PrettyJSONSerializer()
#         authentication = Authentication()
#         authorization = DjangoAuthorization()
#
# class LocationPictureResource(ModelResource):
#     location = fields.ForeignKey(LocationResource, 'location', full=True)
#     class Meta:
#         queryset = LocationPicture.objects.all()
#         resource_name = 'location_picture'
#         filtering = {
#             "location": ALL_WITH_RELATIONS,
#         }
#         serializer = PrettyJSONSerializer()
#         authentication = Authentication()
#         authorization = DjangoAuthorization()

# class ActivityResource(ModelResource):
#     location = fields.ForeignKey(LocationResource, 'location', full=True)
#     member_create = fields.ForeignKey(MemberResource, 'member_create', full=True)
#     member_join = fields.ToManyField(MemberResource, 'member_join', full=True)
#     class Meta:
#         queryset = Activity.objects.all()
#         resource_name = 'activity'
#         filtering = {
#             "location": ALL_WITH_RELATIONS,
#             'start_time': ['exact', 'lt', 'lte', 'gte', 'gt'],
#         }
#         serializer = PrettyJSONSerializer()
#         authentication = Authentication()
#         authorization = DjangoAuthorization()

# class ActivityTodayResource(ModelResource):
#     location = fields.ForeignKey(LocationResource, 'location', full=True)
#     member_create = fields.ForeignKey(MemberResource, 'member_create', full=True)
#     member_join = fields.ToManyField(MemberResource, 'member_join', full=True)
#     class Meta:
#         queryset = Activity.objects.all()
#         resource_name = 'activity_today'
#         filtering = {
#             "location": ALL_WITH_RELATIONS,
#         }
#         serializer = PrettyJSONSerializer()
#         authentication = Authentication()
#         authorization = DjangoAuthorization()    

#     def get_object_list(self, request):    
#         activities_id = get_today_activity(activity_id=True)
#         return super(ActivityTodayResource, self).get_object_list(request).filter(
#                 Q(pk__in=activities_id) 
#             )


# class CommentResource(ModelResource):
#     activity = fields.ForeignKey(ActivityResource, 'activity')
#     class Meta:
#         queryset = Comment.objects.all()
#         resource_name = "comment"
#         filtering = {
#            "comment_type": ("exact",),
#         }
#         ordering = ['created_date']
#         serializer = PrettyJSONSerializer()
#         authentication = Authentication()
#         authorization = DjangoAuthorization()