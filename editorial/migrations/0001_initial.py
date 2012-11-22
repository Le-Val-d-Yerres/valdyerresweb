# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PageBase'
        db.create_table('editorial_pagebase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('meta_description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('contenu', self.gf('django.db.models.fields.TextField')()),
            ('publie', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_mise_a_jour', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('editorial', ['PageBase'])

        # Adding model 'PageStatique'
        db.create_table('editorial_pagestatique', (
            ('pagebase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['editorial.PageBase'], unique=True, primary_key=True)),
            ('date_creation', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('editorial', ['PageStatique'])

        # Adding model 'Actualite'
        db.create_table('editorial_actualite', (
            ('pagebase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['editorial.PageBase'], unique=True, primary_key=True)),
            ('logo', self.gf('filebrowser.fields.FileBrowseField')(max_length=200, null=True, blank=True)),
            ('date_publication', self.gf('django.db.models.fields.DateTimeField')()),
            ('page_accueil', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('editorial', ['Actualite'])

        # Adding model 'DocumentAttache'
        db.create_table('editorial_documentattache', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('document', self.gf('filebrowser.fields.FileBrowseField')(max_length=200)),
            ('reference', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['editorial.PageStatique'])),
        ))
        db.send_create_signal('editorial', ['DocumentAttache'])

        # Adding model 'Magazine'
        db.create_table('editorial_magazine', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('date_parution', self.gf('django.db.models.fields.DateField')()),
            ('document', self.gf('filebrowser.fields.FileBrowseField')(max_length=200)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('editorial', ['Magazine'])

        # Adding model 'RapportActivite'
        db.create_table('editorial_rapportactivite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('date_parution', self.gf('django.db.models.fields.DateField')()),
            ('document', self.gf('filebrowser.fields.FileBrowseField')(max_length=200)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('editorial', ['RapportActivite'])


    def backwards(self, orm):
        # Deleting model 'PageBase'
        db.delete_table('editorial_pagebase')

        # Deleting model 'PageStatique'
        db.delete_table('editorial_pagestatique')

        # Deleting model 'Actualite'
        db.delete_table('editorial_actualite')

        # Deleting model 'DocumentAttache'
        db.delete_table('editorial_documentattache')

        # Deleting model 'Magazine'
        db.delete_table('editorial_magazine')

        # Deleting model 'RapportActivite'
        db.delete_table('editorial_rapportactivite')


    models = {
        'editorial.actualite': {
            'Meta': {'object_name': 'Actualite', '_ormbases': ['editorial.PageBase']},
            'date_publication': ('django.db.models.fields.DateTimeField', [], {}),
            'logo': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'page_accueil': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pagebase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['editorial.PageBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        'editorial.documentattache': {
            'Meta': {'object_name': 'DocumentAttache'},
            'document': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'reference': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['editorial.PageStatique']"})
        },
        'editorial.magazine': {
            'Meta': {'object_name': 'Magazine'},
            'date_parution': ('django.db.models.fields.DateField', [], {}),
            'document': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'titre': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'editorial.pagebase': {
            'Meta': {'object_name': 'PageBase'},
            'contenu': ('django.db.models.fields.TextField', [], {}),
            'date_mise_a_jour': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'publie': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
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
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'titre': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['editorial']