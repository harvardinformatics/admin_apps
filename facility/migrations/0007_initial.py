# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Facility'
        db.create_table('facility_facility', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('logo_filename', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('street', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('street2', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
            ('state', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
            ('zip', self.gf('django.db.models.fields.CharField')(default='', max_length=10)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 2, 14, 0, 0), auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 2, 14, 0, 0), auto_now=True, blank=True)),
        ))
        db.send_create_signal('facility', ['Facility'])


    def backwards(self, orm):
        # Deleting model 'Facility'
        db.delete_table('facility_facility')


    models = {
        'facility.facility': {
            'Meta': {'object_name': 'Facility'},
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 2, 14, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo_filename': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 2, 14, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'street': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'street2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'})
        }
    }

    complete_apps = ['facility']