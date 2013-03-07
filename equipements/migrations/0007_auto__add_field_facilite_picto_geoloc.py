# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Facilite.picto_geoloc'
        db.add_column('equipements_facilite', 'picto_geoloc',
                      self.gf('filebrowser.fields.FileBrowseField')(max_length=200, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Facilite.picto_geoloc'
        db.delete_column('equipements_facilite', 'picto_geoloc')


    models = {
        'equipements.equipement': {
            'Meta': {'ordering': "['ville__nom']", 'object_name': 'Equipement', '_ormbases': ['localisations.Lieu']},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'fonction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['equipements.EquipementFonction']"}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'lieu_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['localisations.Lieu']", 'unique': 'True', 'primary_key': 'True'}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'presentation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'equipements.equipementfonction': {
            'Meta': {'object_name': 'EquipementFonction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'picto': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200'}),
            'pluriel': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['services.Service']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        },
        'equipements.facilite': {
            'Meta': {'ordering': "('importance',)", 'object_name': 'Facilite'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'importance': ('django.db.models.fields.IntegerField', [], {}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'picto': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200'}),
            'picto_geoloc': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        },
        'equipements.facilites': {
            'Meta': {'object_name': 'Facilites'},
            'equipement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['localisations.Lieu']"}),
            'facilites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['equipements.Facilite']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'equipements.tarif': {
            'Meta': {'ordering': "['categorie__index', 'index']", 'object_name': 'Tarif'},
            'categorie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['equipements.TarifCategorie']"}),
            'designation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'info_additionelle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'prix_non_residents': ('django.db.models.fields.FloatField', [], {}),
            'prix_residents': ('django.db.models.fields.FloatField', [], {})
        },
        'equipements.tarifcategorie': {
            'Meta': {'ordering': "['index', 'equipement_fonction__nom']", 'object_name': 'TarifCategorie'},
            'equipement_fonction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['equipements.EquipementFonction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        },
        'localisations.lieu': {
            'Meta': {'ordering': "['ville__nom']", 'object_name': 'Lieu'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rue': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'ville': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['localisations.Ville']"})
        },
        'localisations.ville': {
            'Meta': {'object_name': 'Ville'},
            'code_postal': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'communaute_agglo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lien': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
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

    complete_apps = ['equipements']