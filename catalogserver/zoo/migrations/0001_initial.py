# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'VersionPtr'
        db.create_table('zoo_versionptr', (
            ('votes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('zoo', ['VersionPtr'])

        # Adding model 'Version'
        db.create_table('zoo_version', (
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('versionptr', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['zoo.VersionPtr'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
        ))
        db.send_create_signal('zoo', ['Version'])

        # Adding model 'Spec'
        db.create_table('zoo_spec', (
            ('spec', self.gf('django.db.models.fields.TextField')()),
            ('version', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['zoo.Version'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('summary', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('zoo', ['Spec'])

        # Adding model 'Snippet'
        db.create_table('zoo_snippet', (
            ('code', self.gf('django.db.models.fields.TextField')()),
            ('spec_versionptr', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['zoo.VersionPtr'])),
            ('version', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['zoo.Version'], unique=True, primary_key=True)),
            ('language', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('zoo', ['Snippet'])

        # Adding model 'Vote'
        db.create_table('zoo_vote', (
            ('versionptr', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['zoo.VersionPtr'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('zoo', ['Vote'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'VersionPtr'
        db.delete_table('zoo_versionptr')

        # Deleting model 'Version'
        db.delete_table('zoo_version')

        # Deleting model 'Spec'
        db.delete_table('zoo_spec')

        # Deleting model 'Snippet'
        db.delete_table('zoo_snippet')

        # Deleting model 'Vote'
        db.delete_table('zoo_vote')
    
    
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
        'zoo.snippet': {
            'Meta': {'object_name': 'Snippet'},
            'code': ('django.db.models.fields.TextField', [], {}),
            'language': ('django.db.models.fields.TextField', [], {}),
            'spec_versionptr': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zoo.VersionPtr']"}),
            'version': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['zoo.Version']", 'unique': 'True', 'primary_key': 'True'})
        },
        'zoo.spec': {
            'Meta': {'object_name': 'Spec'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'spec': ('django.db.models.fields.TextField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {}),
            'version': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['zoo.Version']", 'unique': 'True', 'primary_key': 'True'})
        },
        'zoo.version': {
            'Meta': {'object_name': 'Version'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
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
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'value': ('django.db.models.fields.IntegerField', [], {}),
            'versionptr': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zoo.VersionPtr']"})
        }
    }
    
    complete_apps = ['zoo']
