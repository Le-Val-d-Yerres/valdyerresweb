# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cinema'
        db.create_table('cinemas_cinema', (
            ('lieu_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['localisations.Lieu'], unique=True, primary_key=True)),
            ('id_allocine_cine', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('meta_description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('hash_maj', self.gf('django.db.models.fields.CharField')(max_length=42)),
        ))
        db.send_create_signal('cinemas', ['Cinema'])

        # Adding model 'Film'
        db.create_table('cinemas_film', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('id_allocine_film', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('duree', self.gf('django.db.models.fields.IntegerField')()),
            ('url_allocine_image', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal('cinemas', ['Film'])

        # Adding model 'Seance'
        db.create_table('cinemas_seance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('film', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cinemas.Film'])),
            ('cinema', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cinemas.Cinema'])),
            ('id_allocine_film', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_debut', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_fin', self.gf('django.db.models.fields.DateTimeField')()),
            ('format', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('version_lang', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('version_vo', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('cinemas', ['Seance'])


    def backwards(self, orm):
        # Deleting model 'Cinema'
        db.delete_table('cinemas_cinema')

        # Deleting model 'Film'
        db.delete_table('cinemas_film')

        # Deleting model 'Seance'
        db.delete_table('cinemas_seance')


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