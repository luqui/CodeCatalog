# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Deleting model 'Test'
        db.delete_table('zoo_test')

        # Adding field 'Spec.parent'
        db.add_column('zoo_spec', 'parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='child', null=True, to=orm['zoo.Spec']), keep_default=False)

        # Adding field 'Snippet.parent'
        db.add_column('zoo_snippet', 'parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='child', null=True, to=orm['zoo.Snippet']), keep_default=False)

        # Adding field 'Snippet.date'
        db.add_column('zoo_snippet', 'date', self.gf('django.db.models.fields.DateField')(default=datetime.date(2011, 3, 19)), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Adding model 'Test'
        db.create_table('zoo_test', (
            ('code', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('spec', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['zoo.Spec'])),
        ))
        db.send_create_signal('zoo', ['Test'])

        # Deleting field 'Spec.parent'
        db.delete_column('zoo_spec', 'parent_id')

        # Deleting field 'Snippet.parent'
        db.delete_column('zoo_snippet', 'parent_id')

        # Deleting field 'Snippet.date'
        db.delete_column('zoo_snippet', 'date')
    
    
    models = {
        'zoo.snippet': {
            'Meta': {'object_name': 'Snippet'},
            'code': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
