from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from frittie.settings import MEDIA_URL
from friends.models import Friendship
from django.db.models.signals import post_save
from utils import get_elapse_time
from markdown import markdown
from friends.models import Friendship
from django_facebook.models import FacebookProfileModel
import datetime
import random

from django.conf import settings
try:
    storage = settings.MULTI_IMAGES_FOLDER+'/'
except AttributeError:
    storage = 'multiuploader_images/'

########################################
#                                      #
#           CONSTANT DATA              #
#                                      #
########################################
USA_STATES = (
   ("AL","Alabama"),("AK","Alaska"),("AZ","Arizona"),("AR","Arkansas"),("CA","California"),
   ("CO","Colorado"),("CT","Connecticut"),("DE","Delaware"),("FL","Florida"),("GA","Georgia"),
   ("HI","Hawaii"),("ID","Idaho"),("IL","Illinois"),("IN","Indiana"),("IA","Iowa"),
   ("KS","Kansas"),("KY","Kentucky"),("LA","Louisana"),("ME","Maine"),("MD","Maryland"),
   ("MA","Massachusetts"),("MI","Michigan"),("MN","Minnesota"),("MS","Mississippi"),("MO","Missouri"),
   ("MT","Montana"),("NE","Nebraska"),("NV","Nevada"),("NH","New Hampshire"),("NJ","New Jersey"),
   ("NM","New Mexico"),("NY","New York"),("NC","North Carolina"),("ND","North Dakota"),("OH","Ohio"),
   ("OK","Oklahoma"),("OR","Oregon"),("PA","Pennsylvania"),("RI","Rhode Island"),("SC","South Carolina"),
   ("SD","South Dakota"),("TN","Tennessee"),("TX","Texas"),("UT","Utah"),("VT","Vermont"),
   ("VA","Virginia"),("WA","Washington"),("WV","West Virginia"),("WI","Wisconsin"),("WY","Wyoming"),
)

CATEGORY = (
   ("Restaurant","Restaurant"),
   ("Entertaining","Entertaining"),
   ("Shopping","Shopping"),
   ("Outdoor","Outdoor"),
   ("Dating","Dating"),
)

PRIVACY_STATUS = (
	("Public","Public"),
	("Private","Private"),
)

ACTIVITY_STATUS = (
	("Upcoming","Upcoming"),
	("Happening","Happening"),
	("Past","Past"),
)

ACTIVITY_REQUEST_STATUS = (
  ("Accepted", "Acccepted"),
  ("Waiting", "Waiting"),
  ("Decline", "Decline"),
)

ACTIVITY_USER_RELATION_STATUS = (
    ('hide','hide'),
    ('show','show')
  )

STATUS = (
      ("old", "old"),
      ("new", "new"),
    ) 

APPEARANCE_STATUS = (
      ("hide", "hide"),
      ("show", "show"),
    ) 

NOTIFY_TYPE = (
      ('add_friend','add_friend'),
      ('add_friend_response_accept','add_friend_response_accept'),        # Not notice
      ('add_friend_response_decline','add_friend_response_decline'),      # Not notice
      ('friend_request_not_active','friend_request_not_active'),          # Not notice
      ('accept_friend_request','accept_friend_request'),
      ('join_activity_request','join_activity_request'),
      ('accept_activity_request','accept_activity_request'),
      ('decline_activity_request','decline_activity_request'),
      ('cancel_joining_activity','cancel_joining_activity'),  
      ('recommend_location','recommend_location'),
      ('recommend_activity','recommend_activity'),
      ('new_activity_in_location','new_activity_in_location'),
    ) 

# Trending is activity which have a lot of member join
# Hot is activity which have a lot of comment
# ACTIVITY_SPECIAL = (
#       ('Trending','Trending'),
#       ('Hot','Hot'),
#       ('None','None'),
#     )

# LOCATION_SPECIAL = (
#       ('Hot','Hot'),
#       ('Most Rated', 'Most Rated'),
#       ('None','None')
#     )

ACTIVITY_TYPE = (
      ('public','public'),
      ('invite_only','invite_only'),
      ('anonymous','anonymous'),
      ('blind_date','blind_date')
    )

GENDER = (
      ("Male", "Male"),
      ("Female", "Female"),
    )

COMMENT_TYPE = (
      ('activity','activity'),
      ('location','location'),
      ('activity_photo','activity_photo'),
      ('location_photo','location_photo')
    )

FRIT_TYPE = (
      ('activity','activity'),
      ('location','location'),
      ('comment','comment'),
      ('member','member'),
      ('photo','photo')
    )

RECOMMENT_TYPE = (
      ('activity','activity'),
      ('location','location')
    )

REPORT_TYPE = (
      ('comment','comment'),
    )

PHOTO_TYPE = (
      ('activity','activity'),
      ('location','location')
    )

class Frit(models.Model):
    frit_type = models.CharField(max_length=20,choices=FRIT_TYPE)
    object_id = models.IntegerField()
    member = models.ForeignKey("Member")
    date = models.DateTimeField(default=datetime.datetime.now())

class Photo(models.Model):
    filename = models.CharField(max_length=60, blank=True, null=True)
    image = models.FileField(upload_to=storage)
    key_data = models.CharField(max_length=90, unique=True, blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    member_post = models.ForeignKey('Member')
    photo_type = models.CharField(max_length=20,choices=PHOTO_TYPE)
    object_id = models.IntegerField()

    @property
    def key_generate(self):
        """returns a string based unique key with length 80 chars"""
        while 1:
            key = str(random.getrandbits(256))
            try:
                MultiuploaderImage.objects.get(key=key)
            except:
                return key

    def __unicode__(self):
        return self.image.name


class Message(models.Model):
    member_send = models.ForeignKey('Member', related_name='member_send')
    member_receive= models.ForeignKey('Member', related_name='member_receive')
    content = models.TextField()
    content_html = models.TextField(editable=False, blank=True)
    status = models.CharField(max_length=5,choices=STATUS)
    appearance_status = models.CharField(max_length=5,choices=APPEARANCE_STATUS,default='show')
    date = models.DateTimeField(default=datetime.datetime.now())
    elapse_time = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        now = datetime.datetime.now()
        elapse = now - self.date
        self.elapse_time = get_elapse_time(int(elapse.total_seconds())) 
        self.content_html = markdown(self.content.replace("\n","<br>").replace(" ","&nbsp;"))
        super(Message, self).save(*args, **kwargs)

class Recommend(models.Model):
    recommend_type = models.CharField(max_length=20,choices=RECOMMENT_TYPE)
    object_id = models.IntegerField()
    member_send = models.ForeignKey('Member',related_name='member_send_recommend')
    member_receive = models.ManyToManyField('Member',related_name='member_receive_recommend')
    date = models.DateTimeField(default=datetime.datetime.now())    

########################################
#                                      #
#           COMMENT MODEL              #
#                                      #
########################################
class Comment(models.Model):
    comment_type = models.CharField(max_length=20,choices=COMMENT_TYPE)
    object_id = models.IntegerField()
    member = models.ForeignKey("Member")
    content = models.TextField()
    content_html = models.TextField(editable=False, blank=True)
    created_date = models.DateTimeField(default=datetime.datetime.now())
    created_elapse_time = models.CharField(max_length=50)
    edit_date =  models.DateTimeField(blank=True,null=True)
    edit_elapse_time = models.CharField(max_length=50,blank=True,null=True)
    class Meta:
        ordering = ['created_date']
      
    def save(self, *args, **kwargs):
        now = datetime.datetime.now()
        created_elapse = now - self.created_date
        self.created_elapse_time = get_elapse_time(int(created_elapse.total_seconds())) 
        if self.edit_date != None:
            edit_elapse = now - self.edit_date
            self.edit_elapse_time = get_elapse_time(edit_elapse.total_seconds())
        self.content_html = markdown(self.content.replace("\n","<br>").replace(" ","&nbsp;"))
        super(Comment, self).save(*args, **kwargs)


class Report(models.Model):
    report_type = models.CharField(max_length=20,choices=REPORT_TYPE)
    object_id = models.IntegerField()
    member_report = models.ManyToManyField("Member",related_name='member_report',blank=True)
    date = models.DateTimeField(default=datetime.datetime.now())
    reason_content = models.TextField()
    class Meta:
        ordering = ['date']

########################################
#                                      #
#           MEMBER MODEL              #
#                                      #
########################################
class Member(FacebookProfileModel):
    # This field is required.
    user = models.ForeignKey(User, unique=True)
    
    # Additional fields of user
    nickname = models.CharField(max_length=100,blank=True)
    #gender = models.CharField(max_length=10,choices=GENDER,default='Male')
    basic_info = models.TextField(blank=True)
    birthdate = models.DateField(blank=True,null=True)
    avatar = models.ImageField("Profile Picture", upload_to="uploads/img/member/", blank=True, null=True)
    city = models.CharField(max_length=50,blank=True)
    state = models.CharField(max_length=2,choices=USA_STATES,blank=True)
    privacy_status = models.CharField(max_length=10,choices=PRIVACY_STATUS,default='Public')
    def __unicode__(self):
        return unicode(self.user)
    
    def save(self, *args, **kwargs):
        if self.facebook_id == None:
          if self.avatar == None:
            if self.gender == "Male":
              self.avatar = "default/img/male_avatar.gif"
            else:
              self.avatar = "default/img/female_avatar.gif"
        else:
          self.avatar = self.image
        super(Member, self).save(*args, **kwargs)

    def get_friends(self):
        return Member.objects.filter(user__in=User.objects.filter(pk__in=Friendship.objects.friends_of(self.user).values_list('id', flat=True)))

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

########################################
#                                      #
#           NOTIFY MODEL               #
#                                      #
########################################
class Notify(models.Model):
    content = models.TextField()
    status = models.CharField(max_length=3,choices=STATUS,default='new')
    notify_type = models.CharField(max_length=50,choices=NOTIFY_TYPE,null=True)
    notify_to = models.ForeignKey("Member", related_name='notify_to')
    notify_from = models.ForeignKey("Member", related_name='notify_from')
    object_id = models.IntegerField(default=-1)
    date = models.DateTimeField(default=datetime.datetime.now())
    elapse_time = models.CharField(max_length=50)

    # def save(self, *args, **kwargs):
    #     now = datetime.datetime.now()
    #     elapse_time = now - self.date
    #     self.elapse_time = get_elapse_time(int(elapse_time.total_seconds())) 
    #     super(Notify, self).save(*args, **kwargs)

    class Meta:
	     ordering= ['date']

########################################
#                                      #
#           ACTIVITY MODEL             #
#                                      #
########################################
class ActivityRequest(models.Model):
    activity = models.ForeignKey("Activity")
    member_join = models.ForeignKey("Member", related_name='activity_member_join')
    member_create = models.ForeignKey("Member", related_name='activity_member_create')
    date = models.DateTimeField(default=datetime.datetime.now())
    request_status = models.CharField(max_length=10,choices=ACTIVITY_REQUEST_STATUS,default='Waiting')

class ActivityUserRelation(models.Model):
    activity = models.ForeignKey('Activity')
    member = models.ForeignKey('Member')
    status = models.CharField(max_length=20,choices=ACTIVITY_USER_RELATION_STATUS)

class Activity(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    description_html = models.TextField(editable=False, blank=True)
    start_time = models.DateTimeField(default=datetime.datetime.now())
    end_time = models.DateTimeField()
    logo = models.ImageField("Activity Logo", upload_to="uploads/img/activity/", blank=True, default='default/img/activity.jpg')
    member_create = models.ForeignKey("Member", related_name="member_create")          # User who create this activity (one-many)
    member_join = models.ManyToManyField("Member", related_name="member_join",blank=True,null=True)   # List of user who join this activity (many-many)
    member_invite = models.ManyToManyField('Member',related_name='member_invite',blank=True,null=True)
    activity_status = models.CharField(max_length=20,choices=ACTIVITY_STATUS,default='Upcomming')            # Show status (done/happening/coming...)
    location = models.ForeignKey("Location")
    #special = models.CharField(max_length=20,choices=ACTIVITY_SPECIAL,default='None')
    limit = models.IntegerField(default=-1)                       # Limit how many people can join this
    activity_type = models.CharField(max_length=20,choices=ACTIVITY_TYPE,default='public')    # public or private activity
    age_range_start = models.IntegerField(blank=True,null=True)
    age_range_end = models.IntegerField(blank=True,null=True)
    comment_restriction = models.CharField(max_length=20,default='Allow')

    # These two field is used for get_trending_activity and get_hot_activity function
    comment_amount = models.IntegerField(default=0)
    member_join_amount = models.IntegerField(default=0)
    member_invite_amount = models.IntegerField(default=0)
    recomment_amount = models.IntegerField(default=0)
    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        now = datetime.datetime.now()
        if self.start_time > now: self.activity_status = 'Upcoming'
        if self.end_time < now: self.activity_status = 'Past'
        if self.start_time < now and self.end_time > now: self.activity_status = 'Happening'
        self.description_html = markdown(self.description.replace("\n","</br>").replace(" ","&nbsp;"))
        super(Activity, self).save(*args, **kwargs)

    def update_comment_amount(self):
        try:
          self.comment_amount = len(Comment.objects.filter(comment_type='activity',object_id=self.pk))
          self.save()
        except:
          pass

    def update_member_amount(self):
        try:
          self.member_join_amount = len(Activity.objects.get(pk=self.pk).member_join.all())
          self.member_invite_amount = len(Activity.objects.get(pk=self.pk).member_invite.all())
          self.save()
        except:
          pass

    def update_recomment_amount(self):
        try:
          self.recomment_amount = len(Recomment.objects.filter(recomment_type='activity',object_id=self.pk))
          self.save()
        except:
          pass

    class Meta:
        ordering = ['name']

########################################
#                                      #
#           LOCATION MODEL             #
#                                      #
########################################
class Location(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    description_html = models.TextField(editable=False, blank=True)
    category = models.CharField(max_length=30,choices=CATEGORY,default='Restaurant')
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100,blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=20,choices=USA_STATES)
    zip_code = models.IntegerField()
    country = models.CharField(max_length=50,blank=True)
    #url = models.URLField(blank=True)
    rating = models.FloatField(blank=True,default=0.0)
    avatar = models.ImageField("Location Avatar", upload_to="uploads/img/location/",blank=True,default="default/img/location.jpg") 
    create_by = models.ForeignKey("Member", related_name="create_by")
    follow_by = models.ManyToManyField("Member", related_name="follow_by",blank=True,null=True)
    preference = models.TextField(blank=True)
    #special = models.CharField(max_length=20,choices=LOCATION_SPECIAL,default='None')
    comment_amount = models.IntegerField(default=0)
    recommend_amount = models.IntegerField(default=0)

    class Meta:
        ordering = ['name']
    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.description_html = markdown(self.description.replace("\n","</br>").replace(" ","&nbsp;"))
        super(Location, self).save(*args, **kwargs)

    def count_activity(self):
        activities = Activity.objects.filter(location=self)
        return len(activities)

    def get_review(self):
        return Comment.objects.filter(comment_type='location',object_id=self.pk)

    def get_picture(self):
        return Photo.objects.filter(photo_type='location',object_id=self.pk)

    def update_comment_amount(self):
        try:
          self.comment_amount = len(Comment.objects.filter(comment_type='location',object_id=self.pk))
          self.save()
        except:
          pass

    def update_recomment_amount(self):
        try:
          self.recomment_amount = len(Recomment.objects.filter(recomment_type='location',object_id=self.pk))
          self.save()
        except:
          pass

class LocationCategory(models.Model):
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=30)
    description = models.CharField(max_length=200,blank=True)
    icon = models.ImageField("Category Icon", upload_to="uploads/img/main/",blank=True)

class FritLocation(models.Model):
    fritnum = models.IntegerField()
    memberfrit = models.ForeignKey("Member")
    location = models.ForeignKey("Location")

class FritPhoto(models.Model):
    fritnum = models.IntegerField()
    memberfrit = models.ForeignKey("Member")
    photo = models.ForeignKey("Activity")

class FritComment(models.Model):
    fritnum = models.IntegerField()
    memberfrit = models.ForeignKey("Member")
    comment = models.ForeignKey("Comment")

class FritActivity(models.Model):
    fritnum = models.IntegerField()
    memberfrit = models.ForeignKey("Member")
    activity = models.ForeignKey("Activity")

class FritMember(models.Model):
    fritnum = models.IntegerField()
    memberfrit = models.ForeignKey("Member",related_name="memberfrit")
    memberidol = models.ForeignKey("Member",related_name="memberidol")