# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'Snippet.canon'
        db.add_column('zoo_snippet', 'canon', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True), keep_default=False)

        # Adding field 'Snippet.language'
        db.add_column('zoo_snippet', 'language', self.gf('django.db.models.fields.TextField')(default='python'), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Deleting field 'Snippet.canon'
        db.delete_column('zoo_snippet', 'canon')

        # Deleting field 'Snippet.language'
        db.delete_column('zoo_snippet', 'language')
    
    
    models = {
        'zoo.snippet': {
            'Meta': {'object_name': 'Snippet'},
            'canon': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'code': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.TextField', [], {'default': "'python'"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child'", 'null': 'True', 'to': "orm['zoo.Snippet']"}),
            'spec': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zoo.Spec']"})
        },
        'zoo.spec': {
            'Meta': {'object_name': 'Spec'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child'", 'null': 'True', 'to': "orm['zoo.Spec']"}),
            'spec': ('django.db.models.fields.TextField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {})
        }
    }
    
    complete_apps = ['zoo']
