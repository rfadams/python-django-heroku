# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Activity'
        db.delete_table('accounts_activity')

        # Adding model 'NewsItem'
        db.create_table('accounts_newsitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='activity_creator', to=orm['auth.User'])),
            ('receiver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='activity_receiver', to=orm['auth.User'])),
            ('new', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
            ('notification', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('accounts', ['NewsItem'])


    def backwards(self, orm):
        
        # Adding model 'Activity'
        db.create_table('accounts_activity', (
            ('receiver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='activity_receiver', to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('new', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='activity_creator', to=orm['auth.User'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('notification', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
        ))
        db.send_create_signal('accounts', ['Activity'])

        # Deleting model 'NewsItem'
        db.delete_table('accounts_newsitem')


    models = {
        'accounts.founder': {
            'Meta': {'ordering': "['user']", 'object_name': 'Founder'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'projects': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['accounts.Project']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'accounts.newsitem': {
            'Meta': {'ordering': "['-created']", 'object_name': 'NewsItem'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'activity_creator'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'new': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'notification': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'activity_receiver'", 'to': "orm['auth.User']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'accounts.project': {
            'Meta': {'ordering': "['-modified']", 'object_name': 'Project'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
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
        }
    }

    complete_apps = ['accounts']
