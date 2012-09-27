from frittie.app.main.models import *
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


########################################
#                                      #
#      DEFINE CLASS ADMIN AREA         #
#                                      #
########################################
  

class MemberAdmin(admin.ModelAdmin):
    list_display = ['user','gender','avatar','basic_info','city','state','birthdate']

class MessageAdmin(admin.ModelAdmin):
    list_display = ['member_receive','member_send', 'content','content_html','date','status']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment_type','object_id','member','content','content_html','created_date','created_elapse_time','edit_date','edit_elapse_time']

class ReportAdmin(admin.ModelAdmin):
    list_display = ['report_type','object_id','date']

class ActivityRequestAdmin(admin.ModelAdmin):
    list_display = ['activity','member_join','member_create','date','request_status']

class ActivityAdmin(admin.ModelAdmin):
    list_display = ['name','description','description_html','start_time','end_time','logo',
                    'member_create','activity_status','activity_type','location','limit']
    
class ActivityUserRelationAdmin(admin.ModelAdmin):
    list_display = ['activity','member','status']

class LocationAdmin(admin.ModelAdmin):
    list_display = ['name','description','create_by','category','rating','address1','address2','city','state','zip_code','country','avatar']
    search_fields = ['name','category','zip_code','state','country']

class NotifyAdmin(admin.ModelAdmin):
    list_display = ['notify_type','content','notify_to','notify_from','date','status']

class LocationCategoryAdmin(admin.ModelAdmin):
    list_display = ['name','value','description','icon']

class PhotoAdmin(admin.ModelAdmin):
    search_fields = ["filename",'photo_type','member_post']
    list_display = ["filename",'photo_type','object_id','member_post','upload_date']
    list_filter = ["filename",'photo_type','object_id','member_post','upload_date']

class RecommendAdmin(admin.ModelAdmin):
    list_display = ['recommend_type','object_id','member_send']

class FritLocationAdmin(admin.ModelAdmin):
    search_field=['fritnum','memberfrit','location']
    list_display=['fritnum','memberfrit','location']

class FritCommentAdmin(admin.ModelAdmin):
    search_field=['fritnum','memberfrit','comment']
    list_display=['fritnum','memberfrit','comment']

class FritPhotoAdmin(admin.ModelAdmin):
    search_field=['fritnum','memberfrit','photo']
    list_display=['fritnum','memberfrit','photo']

class FritActivityAdmin(admin.ModelAdmin):
    search_field=['fritnum','memberfrit','activity']
    list_display=['fritnum','memberfrit','activity']

class FritMemberAdmin(admin.ModelAdmin):
    search_field=['fritnum','memberfrit','memberidol']
    list_display=['fritnum','memberfrit','memberidol']
########################################
#                                      #
#     	     REGISTER AREA             #
#                                      #
########################################
admin.site.register(Member, MemberAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Notify, NotifyAdmin)
admin.site.register(LocationCategory, LocationCategoryAdmin)
admin.site.register(ActivityRequest,ActivityRequestAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Message,MessageAdmin)
admin.site.register(Recommend,RecommendAdmin)
admin.site.register(FritLocation,FritLocationAdmin)
admin.site.register(FritComment,FritCommentAdmin)
admin.site.register(FritPhoto,FritPhotoAdmin)
admin.site.register(FritActivity,FritActivityAdmin)
admin.site.register(FritMember,FritMemberAdmin)

