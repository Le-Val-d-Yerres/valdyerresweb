# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ImportGIDEM.fichier_xls'
        db.alter_column('annoncesemploi_importgidem', 'fichier_xls', self.gf('django.db.models.fields.files.FileField')(max_length=100))

    def backwards(self, orm):

        # Changing field 'ImportGIDEM.fichier_xls'
        db.alter_column('annoncesemploi_importgidem', 'fichier_xls', self.gf('filebrowser.fields.FileBrowseField')(max_length=200))

    models = {
        'annoncesemploi.annonce': {
            'Meta': {'object_name': 'Annonce'},
            'contact': ('django.db.models.fields.TextField', [], {}),
            'deplacement': ('django.db.models.fields.TextField', [], {}),
            'description_du_poste': ('django.db.models.fields.TextField', [], {}),
            'experience_requise': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intitule': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'lieu_travail': ('django.db.models.fields.TextField', [], {}),
            'nb_postes': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'niveau_formation': ('django.db.models.fields.TextField', [], {}),
            'nom_employeur': ('django.db.models.fields.TextField', [], {}),
            'publie': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'salaire_indicatif': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'secteur_activite': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['services.Service']", 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'type_de_poste': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'annoncesemploi.importgidem': {
            'Meta': {'object_name': 'ImportGIDEM'},
            'date_import': ('django.db.models.fields.DateTimeField', [], {}),
            'fichier_xls': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'services.service': {
            'Meta': {'object_name': 'Service'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['services.Service']", 'null': 'True', 'blank': 'True'}),
            'publie': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['annoncesemploi']