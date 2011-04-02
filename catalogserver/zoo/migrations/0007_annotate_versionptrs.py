# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from zoo.models import VersionPtr

class Migration(DataMigration):
    
    def forwards(self, orm):
        for vptr in orm.VersionPtr.objects.all():
            versions = orm.Version.objects.filter(versionptr=vptr)
            if not versions.exists(): continue
            version = versions[0]
            vptr.type = -1
            if orm.Spec.objects.filter(version=version).exists():
                vptr.type = VersionPtr.PTRTYPE_TO_ID['Spec']
            elif orm.Snippet.objects.filter(version=version).exists():
                vptr.type = VersionPtr.PTRTYPE_TO_ID['Snippet']
            elif orm.BugReport.objects.filter(version=version).exists():
                vptr.type = VersionPtr.PTRTYPE_TO_ID['BugReport']
            vptr.save()
            
    
    def backwards(self, orm):
        for vptr in orm.VersionPtr.objects.all():
            vptr.type = -1
            vptr.save()
    
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
            'type': ('django.db.models.fields.IntegerField', [], {}),
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
