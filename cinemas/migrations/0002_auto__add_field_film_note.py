# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Film.note'
        db.add_column('cinemas_film', 'note',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Film.note'
        db.delete_column('cinemas_film', 'note')


    models = {
        'cinemas.cinema': {
            'Meta': {'ordering': "['ville__nom']", 'object_name': 'Cinema', '_ormbases': ['localisations.Lieu']},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hash_maj': ('django.db.models.fields.CharField', [], {'max_length': '42'}),
            'id_allocine_cine': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'lieu_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['localisations.Lieu']", 'unique': 'True', 'primary_key': 'True'}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'cinemas.film': {
            'Meta': {'object_name': 'Film'},
            'duree': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_allocine_film': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'titre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_allocine_image': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'cinemas.seance': {
            'Meta': {'object_name': 'Seance'},
            'cinema': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cinemas.Cinema']"}),
            'date_debut': ('django.db.models.fields.DateTimeField', [], {}),
            'date_fin': ('django.db.models.fields.DateTimeField', [], {}),
            'film': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cinemas.Film']"}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_allocine_film': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'version_lang': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'version_vo': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
        }
    }

    complete_apps = ['cinemas']