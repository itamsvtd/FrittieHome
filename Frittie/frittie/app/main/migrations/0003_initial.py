# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Frit'
        db.create_table('main_frit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('frit_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('object_id', self.gf('django.db.models.fields.IntegerField')()),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Member'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 8, 18, 0, 0))),
        ))
        db.send_create_signal('main', ['Frit'])

        # Adding model 'Photo'
        db.create_table('main_photo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('key_data', self.gf('django.db.models.fields.CharField')(max_length=90, unique=True, null=True, blank=True)),
            ('upload_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('member_post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Member'])),
            ('photo_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('object_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('main', ['Photo'])

        # Adding model 'Message'
        db.create_table('main_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member_send', self.gf('django.db.models.fields.related.ForeignKey')(related_name='member_send', to=orm['main.Member'])),
            ('member_receive', self.gf('django.db.models.fields.related.ForeignKey')(related_name='member_receive', to=orm['main.Member'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('content_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('appearance_status', self.gf('django.db.models.fields.CharField')(default='show', max_length=5)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 8, 18, 0, 0))),
            ('elapse_time', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('main', ['Message'])

        # Adding model 'Recommend'
        db.create_table('main_recommend', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recommend_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('object_id', self.gf('django.db.models.fields.IntegerField')()),
            ('member_send', self.gf('django.db.models.fields.related.ForeignKey')(related_name='member_send_recommend', to=orm['main.Member'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 8, 18, 0, 0))),
        ))
        db.send_create_signal('main', ['Recommend'])

        # Adding M2M table for field member_receive on 'Recommend'
        db.create_table('main_recommend_member_receive', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('recommend', models.ForeignKey(orm['main.recommend'], null=False)),
            ('member', models.ForeignKey(orm['main.member'], null=False))
        ))
        db.create_unique('main_recommend_member_receive', ['recommend_id', 'member_id'])

        # Adding model 'Comment'
        db.create_table('main_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comment_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('object_id', self.gf('django.db.models.fields.IntegerField')()),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Member'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('content_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 8, 18, 0, 0))),
            ('created_elapse_time', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('edit_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('edit_elapse_time', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('main', ['Comment'])

        # Adding model 'Report'
        db.create_table('main_report', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('object_id', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 8, 18, 0, 0))),
            ('reason_content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('main', ['Report'])

        # Adding M2M table for field member_report on 'Report'
        db.create_table('main_report_member_report', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('report', models.ForeignKey(orm['main.report'], null=False)),
            ('member', models.ForeignKey(orm['main.member'], null=False))
        ))
        db.create_unique('main_report_member_report', ['report_id', 'member_id'])

        # Adding model 'Member'
        db.create_table('main_member', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('about_me', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('facebook_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True, null=True, blank=True)),
            ('access_token', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('facebook_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('facebook_profile_url', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('website_url', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('blog_url', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('raw_data', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('basic_info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('birthdate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('privacy_status', self.gf('django.db.models.fields.CharField')(default='Public', max_length=10)),
        ))
        db.send_create_signal('main', ['Member'])

        # Adding model 'Notify'
        db.create_table('main_notify', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('django.db.models.fields.CharField')(default='new', max_length=3)),
            ('notify_type', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('notify_to', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notify_to', to=orm['main.Member'])),
            ('notify_from', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notify_from', to=orm['main.Member'])),
            ('object_id', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 8, 18, 0, 0))),
            ('elapse_time', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('main', ['Notify'])

        # Adding model 'ActivityRequest'
        db.create_table('main_activityrequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Activity'])),
            ('member_join', self.gf('django.db.models.fields.related.ForeignKey')(related_name='activity_member_join', to=orm['main.Member'])),
            ('member_create', self.gf('django.db.models.fields.related.ForeignKey')(related_name='activity_member_create', to=orm['main.Member'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 8, 18, 0, 0))),
            ('request_status', self.gf('django.db.models.fields.CharField')(default='Waiting', max_length=10)),
        ))
        db.send_create_signal('main', ['ActivityRequest'])

        # Adding model 'ActivityUserRelation'
        db.create_table('main_activityuserrelation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Activity'])),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Member'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('main', ['ActivityUserRelation'])

        # Adding model 'Activity'
        db.create_table('main_activity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 8, 18, 0, 0))),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(default='default/img/activity.jpg', max_length=100, blank=True)),
            ('member_create', self.gf('django.db.models.fields.related.ForeignKey')(related_name='member_create', to=orm['main.Member'])),
            ('activity_status', self.gf('django.db.models.fields.CharField')(default='Upcomming', max_length=20)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Location'])),
            ('limit', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('activity_type', self.gf('django.db.models.fields.CharField')(default='public', max_length=20)),
            ('age_range_start', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('age_range_end', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('comment_restriction', self.gf('django.db.models.fields.CharField')(default='Allow', max_length=20)),
            ('comment_amount', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('member_join_amount', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('member_invite_amount', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('recomment_amount', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('main', ['Activity'])

        # Adding M2M table for field member_join on 'Activity'
        db.create_table('main_activity_member_join', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['main.activity'], null=False)),
            ('member', models.ForeignKey(orm['main.member'], null=False))
        ))
        db.create_unique('main_activity_member_join', ['activity_id', 'member_id'])

        # Adding M2M table for field member_invite on 'Activity'
        db.create_table('main_activity_member_invite', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['main.activity'], null=False)),
            ('member', models.ForeignKey(orm['main.member'], null=False))
        ))
        db.create_unique('main_activity_member_invite', ['activity_id', 'member_id'])

        # Adding model 'Location'
        db.create_table('main_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('category', self.gf('django.db.models.fields.CharField')(default='Restaurant', max_length=30)),
            ('address1', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('zip_code', self.gf('django.db.models.fields.IntegerField')()),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('rating', self.gf('django.db.models.fields.FloatField')(default=0.0, blank=True)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(default='default/img/location.jpg', max_length=100, blank=True)),
            ('create_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='create_by', to=orm['main.Member'])),
            ('preference', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('comment_amount', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('recommend_amount', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('main', ['Location'])

        # Adding M2M table for field follow_by on 'Location'
        db.create_table('main_location_follow_by', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('location', models.ForeignKey(orm['main.location'], null=False)),
            ('member', models.ForeignKey(orm['main.member'], null=False))
        ))
        db.create_unique('main_location_follow_by', ['location_id', 'member_id'])

        # Adding model 'LocationCategory'
        db.create_table('main_locationcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('main', ['LocationCategory'])

        # Adding model 'FritLocation'
        db.create_table('main_fritlocation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fritnum', self.gf('django.db.models.fields.IntegerField')()),
            ('memberfrit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Member'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Location'])),
        ))
        db.send_create_signal('main', ['FritLocation'])

        # Adding model 'FritPhoto'
        db.create_table('main_fritphoto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fritnum', self.gf('django.db.models.fields.IntegerField')()),
            ('memberfrit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Member'])),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Activity'])),
        ))
        db.send_create_signal('main', ['FritPhoto'])

        # Adding model 'FritComment'
        db.create_table('main_fritcomment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fritnum', self.gf('django.db.models.fields.IntegerField')()),
            ('memberfrit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Member'])),
            ('comment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Comment'])),
        ))
        db.send_create_signal('main', ['FritComment'])

        # Adding model 'FritActivity'
        db.create_table('main_fritactivity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fritnum', self.gf('django.db.models.fields.IntegerField')()),
            ('memberfrit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Member'])),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Activity'])),
        ))
        db.send_create_signal('main', ['FritActivity'])

        # Adding model 'FritMember'
        db.create_table('main_fritmember', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fritnum', self.gf('django.db.models.fields.IntegerField')()),
            ('memberfrit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='memberfrit', to=orm['main.Member'])),
            ('memberidol', self.gf('django.db.models.fields.related.ForeignKey')(related_name='memberidol', to=orm['main.Member'])),
        ))
        db.send_create_signal('main', ['FritMember'])


    def backwards(self, orm):
        # Deleting model 'Frit'
        db.delete_table('main_frit')

        # Deleting model 'Photo'
        db.delete_table('main_photo')

        # Deleting model 'Message'
        db.delete_table('main_message')

        # Deleting model 'Recommend'
        db.delete_table('main_recommend')

        # Removing M2M table for field member_receive on 'Recommend'
        db.delete_table('main_recommend_member_receive')

        # Deleting model 'Comment'
        db.delete_table('main_comment')

        # Deleting model 'Report'
        db.delete_table('main_report')

        # Removing M2M table for field member_report on 'Report'
        db.delete_table('main_report_member_report')

        # Deleting model 'Member'
        db.delete_table('main_member')

        # Deleting model 'Notify'
        db.delete_table('main_notify')

        # Deleting model 'ActivityRequest'
        db.delete_table('main_activityrequest')

        # Deleting model 'ActivityUserRelation'
        db.delete_table('main_activityuserrelation')

        # Deleting model 'Activity'
        db.delete_table('main_activity')

        # Removing M2M table for field member_join on 'Activity'
        db.delete_table('main_activity_member_join')

        # Removing M2M table for field member_invite on 'Activity'
        db.delete_table('main_activity_member_invite')

        # Deleting model 'Location'
        db.delete_table('main_location')

        # Removing M2M table for field follow_by on 'Location'
        db.delete_table('main_location_follow_by')

        # Deleting model 'LocationCategory'
        db.delete_table('main_locationcategory')

        # Deleting model 'FritLocation'
        db.delete_table('main_fritlocation')

        # Deleting model 'FritPhoto'
        db.delete_table('main_fritphoto')

        # Deleting model 'FritComment'
        db.delete_table('main_fritcomment')

        # Deleting model 'FritActivity'
        db.delete_table('main_fritactivity')

        # Deleting model 'FritMember'
        db.delete_table('main_fritmember')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.activity': {
            'Meta': {'ordering': "['name']", 'object_name': 'Activity'},
            'activity_status': ('django.db.models.fields.CharField', [], {'default': "'Upcomming'", 'max_length': '20'}),
            'activity_type': ('django.db.models.fields.CharField', [], {'default': "'public'", 'max_length': '20'}),
            'age_range_end': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'age_range_start': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'comment_amount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'comment_restriction': ('django.db.models.fields.CharField', [], {'default': "'Allow'", 'max_length': '20'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Location']"}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'default': "'default/img/activity.jpg'", 'max_length': '100', 'blank': 'True'}),
            'member_create': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'member_create'", 'to': "orm['main.Member']"}),
            'member_invite': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'member_invite'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['main.Member']"}),
            'member_invite_amount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'member_join': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'member_join'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['main.Member']"}),
            'member_join_amount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'recomment_amount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 18, 0, 0)'})
        },
        'main.activityrequest': {
            'Meta': {'object_name': 'ActivityRequest'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Activity']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 18, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member_create': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'activity_member_create'", 'to': "orm['main.Member']"}),
            'member_join': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'activity_member_join'", 'to': "orm['main.Member']"}),
            'request_status': ('django.db.models.fields.CharField', [], {'default': "'Waiting'", 'max_length': '10'})
        },
        'main.activityuserrelation': {
            'Meta': {'object_name': 'ActivityUserRelation'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Activity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Member']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'main.comment': {
            'Meta': {'ordering': "['created_date']", 'object_name': 'Comment'},
            'comment_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 18, 0, 0)'}),
            'created_elapse_time': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'edit_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'edit_elapse_time': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Member']"}),
            'object_id': ('django.db.models.fields.IntegerField', [], {})
        },
        'main.frit': {
            'Meta': {'object_name': 'Frit'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 18, 0, 0)'}),
            'frit_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Member']"}),
            'object_id': ('django.db.models.fields.IntegerField', [], {})
        },
        'main.fritactivity': {
            'Meta': {'object_name': 'FritActivity'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Activity']"}),
            'fritnum': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memberfrit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Member']"})
        },
        'main.fritcomment': {
            'Meta': {'object_name': 'FritComment'},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Comment']"}),
            'fritnum': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memberfrit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Member']"})
        },
        'main.fritlocation': {
            'Meta': {'object_name': 'FritLocation'},
            'fritnum': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Location']"}),
            'memberfrit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Member']"})
        },
        'main.fritmember': {
            'Meta': {'object_name': 'FritMember'},
            'fritnum': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memberfrit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'memberfrit'", 'to': "orm['main.Member']"}),
            'memberidol': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'memberidol'", 'to': "orm['main.Member']"})
        },
        'main.fritphoto': {
            'Meta': {'object_name': 'FritPhoto'},
            'fritnum': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memberfrit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Member']"}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Activity']"})
        },
        'main.location': {
            'Meta': {'ordering': "['name']", 'object_name': 'Location'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'default': "'default/img/location.jpg'", 'max_length': '100', 'blank': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'default': "'Restaurant'", 'max_length': '30'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'comment_amount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'create_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'create_by'", 'to': "orm['main.Member']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'follow_by': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'follow_by'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['main.Member']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'preference': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'rating': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'blank': 'True'}),
            'recommend_amount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'zip_code': ('django.db.models.fields.IntegerField', [], {})
        },
        'main.locationcategory': {
            'Meta': {'object_name': 'LocationCategory'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'main.member': {
            'Meta': {'object_name': 'Member'},
            'about_me': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'access_token': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'basic_info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'birthdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'blog_url': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'facebook_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'facebook_profile_url': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'privacy_status': ('django.db.models.fields.CharField', [], {'default': "'Public'", 'max_length': '10'}),
            'raw_data': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'website_url': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'main.message': {
            'Meta': {'object_name': 'Message'},
            'appearance_status': ('django.db.models.fields.CharField', [], {'default': "'show'", 'max_length': '5'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 18, 0, 0)'}),
            'elapse_time': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member_receive': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'member_receive'", 'to': "orm['main.Member']"}),
            'member_send': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'member_send'", 'to': "orm['main.Member']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'main.notify': {
            'Meta': {'ordering': "['date']", 'object_name': 'Notify'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 18, 0, 0)'}),
            'elapse_time': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notify_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notify_from'", 'to': "orm['main.Member']"}),
            'notify_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notify_to'", 'to': "orm['main.Member']"}),
            'notify_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '3'})
        },
        'main.photo': {
            'Meta': {'object_name': 'Photo'},
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'key_data': ('django.db.models.fields.CharField', [], {'max_length': '90', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'member_post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Member']"}),
            'object_id': ('django.db.models.fields.IntegerField', [], {}),
            'photo_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'upload_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'main.recommend': {
            'Meta': {'object_name': 'Recommend'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 18, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member_receive': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'member_receive_recommend'", 'symmetrical': 'False', 'to': "orm['main.Member']"}),
            'member_send': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'member_send_recommend'", 'to': "orm['main.Member']"}),
            'object_id': ('django.db.models.fields.IntegerField', [], {}),
            'recommend_type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'main.report': {
            'Meta': {'ordering': "['date']", 'object_name': 'Report'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 18, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member_report': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'member_report'", 'blank': 'True', 'to': "orm['main.Member']"}),
            'object_id': ('django.db.models.fields.IntegerField', [], {}),
            'reason_content': ('django.db.models.fields.TextField', [], {}),
            'report_type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['main']