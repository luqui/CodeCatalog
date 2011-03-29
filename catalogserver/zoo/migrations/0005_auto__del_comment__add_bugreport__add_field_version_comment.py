# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Deleting model 'Comment'
        db.delete_table('zoo_comment')

        # Adding model 'BugReport'
        db.create_table('zoo_bugreport', (
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('target_versionptr', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['zoo.VersionPtr'])),
            ('version', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['zoo.Version'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('zoo', ['BugReport'])

        # Adding field 'Version.comment'
        db.add_column('zoo_version', 'comment', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Adding model 'Comment'
        db.create_table('zoo_comment', (
            ('versionptr', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['zoo.VersionPtr'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('zoo', ['Comment'])

        # Deleting model 'BugReport'
        db.delete_table('zoo_bugreport')

        # Deleting field 'Version.comment'
        db.delete_column('zoo_version', 'comment')
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'zoo.bugreport': {
            'Meta': {'object_name': 'BugReport'},
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'target_versionptr': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zoo.VersionPtr']"}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'version': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['zoo.Version']", 'unique': 'True', 'primary_key': 'True'})
        },
        'zoo.dependency': {
            'Meta': {'object_name': 'Dependency'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'snippet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zoo.Snippet']"}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zoo.VersionPtr']"})
        },
        'zoo.snippet': {
            'Meta': {'object_name': 'Snippet'},
            'code': ('django.db.models.fields.TextField', [], {}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'spec_versionptr': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zoo.VersionPtr']"}),
            'version': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['zoo.Version']", 'unique': 'True', 'primary_key': 'True'})
        },
        'zoo.spec': {
            'Meta': {'object_name': 'Spec'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'spec': ('django.db.models.fields.TextField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {}),
            'version': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['zoo.Version']", 'unique': 'True', 'primary_key': 'True'})
        },
        'zoo.version': {
            'Meta': {'object_name': 'Version'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'versionptr': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zoo.VersionPtr']"})
        },
        'zoo.versionptr': {
            'Meta': {'object_name': 'VersionPtr'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'zoo.vote': {
            'Meta': {'object_name': 'Vote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'value': ('django.db.models.fields.IntegerField', [], {}),
            'versionptr': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zoo.VersionPtr']"})
        }
    }
    
    complete_apps = ['zoo']
