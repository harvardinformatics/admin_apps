# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Invoice'
        db.create_table('invoice_invoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('invoice_number', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('bill_month', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('expense_code_root', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True)),
            ('html_content', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 6, 24, 0, 0))),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 6, 24, 0, 0))),
        ))
        db.send_create_signal('invoice', ['Invoice'])


    def backwards(self, orm):
        # Deleting model 'Invoice'
        db.delete_table('invoice_invoice')


    models = {
        'invoice.invoice': {
            'Meta': {'object_name': 'Invoice'},
            'bill_month': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 24, 0, 0)'}),
            'expense_code_root': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'html_content': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 24, 0, 0)'})
        }
    }

    complete_apps = ['invoice']