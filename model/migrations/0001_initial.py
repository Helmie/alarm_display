# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Station'
        db.create_table(u'model_station', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'model', ['Station'])

        # Adding model 'EngineType'
        db.create_table(u'model_enginetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'model', ['EngineType'])

        # Adding model 'Engine'
        db.create_table(u'model_engine', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('station', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['model.Station'])),
            ('engine_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['model.EngineType'])),
            ('seq_number', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'model', ['Engine'])

        # Adding model 'Mission'
        db.create_table(u'model_mission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('statement', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('issue', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('horn', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'model', ['Mission'])

        # Adding M2M table for field engines on 'Mission'
        m2m_table_name = db.shorten_name(u'model_mission_engines')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mission', models.ForeignKey(orm[u'model.mission'], null=False)),
            ('engine', models.ForeignKey(orm[u'model.engine'], null=False))
        ))
        db.create_unique(m2m_table_name, ['mission_id', 'engine_id'])


    def backwards(self, orm):
        # Deleting model 'Station'
        db.delete_table(u'model_station')

        # Deleting model 'EngineType'
        db.delete_table(u'model_enginetype')

        # Deleting model 'Engine'
        db.delete_table(u'model_engine')

        # Deleting model 'Mission'
        db.delete_table(u'model_mission')

        # Removing M2M table for field engines on 'Mission'
        db.delete_table(db.shorten_name(u'model_mission_engines'))


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
            'number': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['model']