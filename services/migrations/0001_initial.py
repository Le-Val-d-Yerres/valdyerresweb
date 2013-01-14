# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Service'
        db.create_table('services_service', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('index', self.gf('django.db.models.fields.IntegerField')()),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['services.Service'], null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('services', ['Service'])

        # Adding model 'PageStatiqueService'
        db.create_table('services_pagestatiqueservice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['services.Service'])),
            ('titre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('meta_description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('contenu', self.gf('django.db.models.fields.TextField')()),
            ('publie', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('index', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('services', ['PageStatiqueService'])

        # Adding model 'DocumentAttache'
        db.create_table('services_documentattache', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('document', self.gf('filebrowser.fields.FileBrowseField')(max_length=200)),
            ('reference', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['services.PageStatiqueService'])),
        ))
        db.send_create_signal('services', ['DocumentAttache'])


    def backwards(self, orm):
        # Deleting model 'Service'
        db.delete_table('services_service')

        # Deleting model 'PageStatiqueService'
        db.delete_table('services_pagestatiqueservice')

        # Deleting model 'DocumentAttache'
        db.delete_table('services_documentattache')


    models = {
        'services.documentattache': {
            'Meta': {'object_name': 'DocumentAttache'},
            'document': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'reference': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['services.PageStatiqueService']"})
        },
        'services.pagestatiqueservice': {
            'Meta': {'object_name': 'PageStatiqueService'},
            'contenu': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'publie': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['services.Service']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'titre': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'services.service': {
            'Meta': {'object_name': 'Service'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['services.Service']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['services']