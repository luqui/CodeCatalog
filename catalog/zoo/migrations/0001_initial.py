# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Spec'
        db.create_table('zoo_spec', (
            ('spec', self.gf('django.db.models.fields.TextField')()),
            ('summary', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('zoo', ['Spec'])

        # Adding model 'Snippet'
        db.create_table('zoo_snippet', (
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('code', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('spec', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['zoo.Spec'])),
        ))
        db.send_create_signal('zoo', ['Snippet'])

        # Adding model 'Test'
        db.create_table('zoo_test', (
            ('code', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('spec', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['zoo.Spec'])),
        ))
        db.send_create_signal('zoo', ['Test'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Spec'
        db.delete_table('zoo_spec')

        # Deleting model 'Snippet'
        db.delete_table('zoo_snippet')

        # Deleting model 'Test'
        db.delete_table('zoo_test')
    
    
    models = {
        'zoo.snippet': {
            'Meta': {'object_name': 'Snippet'},
            'code': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'spec': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zoo.Spec']"})
        },
        'zoo.spec': {
            'Meta': {'object_name': 'Spec'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'spec': ('django.db.models.fields.TextField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {})
        },
        'zoo.test': {
            'Meta': {'object_name': 'Test'},
            'code': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'spec': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zoo.Spec']"})
        }
    }
    
    complete_apps = ['zoo']
