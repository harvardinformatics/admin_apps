# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Facility.created'
        db.delete_column('facility_facility', 'created')

        # Deleting field 'Facility.modified'
        db.delete_column('facility_facility', 'modified')


    def backwards(self, orm):
        # Adding field 'Facility.created'
        db.add_column('facility_facility', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 2, 14, 0, 0), auto_now_add=True, blank=True),
                      keep_default=False)

        # Adding field 'Facility.modified'
        db.add_column('facility_facility', 'modified',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 2, 14, 0, 0), auto_now=True, blank=True),
                      keep_default=False)


    models = {
        'facility.facility': {
            'Meta': {'object_name': 'Facility'},
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo_filename': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'street': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'street2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'})
        }
    }

    complete_apps = ['facility']