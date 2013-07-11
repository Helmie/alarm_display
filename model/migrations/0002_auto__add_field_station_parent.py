# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Station.parent'
        db.add_column(u'model_station', 'parent',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['model.Station'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Station.parent'
        db.delete_column(u'model_station', 'parent_id')


    models = {
        u'model.engine': {
            'Meta': {'object_name': 'Engine'},
            'engine_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['model.EngineType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'seq_number': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'station': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['model.Station']"})
        },
        u'model.enginetype': {
            'Meta': {'object_name': 'EngineType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'model.mission': {
            'Meta': {'object_name': 'Mission'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'engines': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['model.Engine']", 'symmetrical': 'False'}),
            'horn': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'issue': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'statement': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'model.station': {
            'Meta': {'object_name': 'Station'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['model.Station']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['model']