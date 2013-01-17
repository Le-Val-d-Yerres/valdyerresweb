# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'DocumentAttache.reference'
        db.alter_column('editorial_documentattache', 'reference_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['editorial.PageBase']))
        # Deleting field 'Actualite.logo'
        db.delete_column('editorial_actualite', 'logo')

        # Adding field 'Actualite.image'
        db.add_column('editorial_actualite', 'image',
                      self.gf('filebrowser.fields.FileBrowseField')(max_length=200, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):

        # Changing field 'DocumentAttache.reference'
        db.alter_column('editorial_documentattache', 'reference_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['editorial.PageStatique']))
        # Adding field 'Actualite.logo'
        db.add_column('editorial_actualite', 'logo',
                      self.gf('filebrowser.fields.FileBrowseField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Actualite.image'
        db.delete_column('editorial_actualite', 'image')


    models = {
        'editorial.actualite': {
            'Meta': {'object_name': 'Actualite', '_ormbases': ['editorial.PageBase']},
            'date_publication': ('django.db.models.fields.DateTimeField', [], {}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'page_accueil': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pagebase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['editorial.PageBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        'editorial.documentattache': {
            'Meta': {'object_name': 'DocumentAttache'},
            'document': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'reference': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['editorial.PageBase']"})
        },
        'editorial.magazine': {
            'Meta': {'object_name': 'Magazine'},
            'date_parution': ('django.db.models.fields.DateField', [], {}),
            'document': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'publie': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'titre': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'editorial.pagebase': {
            'Meta': {'object_name': 'PageBase'},
            'contenu': ('django.db.models.fields.TextField', [], {}),
            'date_mise_a_jour': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'publie': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'titre': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'editorial.pagestatique': {
            'Meta': {'object_name': 'PageStatique', '_ormbases': ['editorial.PageBase']},
            'date_creation': ('django.db.models.fields.DateTimeField', [], {}),
            'pagebase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['editorial.PageBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        'editorial.rapportactivite': {
            'Meta': {'object_name': 'RapportActivite'},
            'date_parution': ('django.db.models.fields.DateField', [], {}),
            'document': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'publie': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'titre': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['editorial']