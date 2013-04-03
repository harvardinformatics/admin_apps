# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Facility.street2'
        db.alter_column('facility_facility', 'street2', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

    def backwards(self, orm):

        # Changing field 'Facility.street2'
        db.alter_column('facility_facility', 'street2', self.gf('django.db.models.fields.CharField')(max_length=100))

    models = {
        'facility.facility': {
            'Meta': {'object_name': 'Facility'},
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo_filename': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'street': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'street2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'})
        }
    }

    complete_apps = ['facility']