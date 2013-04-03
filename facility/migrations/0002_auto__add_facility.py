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
            ('street2', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('city', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
            ('state', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
            ('zip', self.gf('django.db.models.fields.CharField')(default='', max_length=10)),
        ))
        db.send_create_signal('facility', ['Facility'])


    def backwards(self, orm):
        # Deleting model 'Facility'
        db.delete_table('facility_facility')


    models = {
        'facility.facility': {
            'Meta': {'object_name': 'Facility'},
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo_filename': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'street': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'street2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'zip': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'})
        }
    }

    complete_apps = ['facility']