# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Evenement.url_reservation'
        db.add_column('evenements_evenement', 'url_reservation',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True),
                      keep_default=False)


        # Changing field 'Evenement.url'
        db.alter_column('evenements_evenement', 'url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True))

    def backwards(self, orm):
        # Deleting field 'Evenement.url_reservation'
        db.delete_column('evenements_evenement', 'url_reservation')


        # Changing field 'Evenement.url'
        db.alter_column('evenements_evenement', 'url', self.gf('django.db.models.fields.URLField')(default='', max_length=200))

    models = {
        'evenements.evenement': {
            'Meta': {'object_name': 'Evenement'},
            'cadre_evenement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['evenements.Saison']"}),
            'debut': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'fin': ('django.db.models.fields.DateTimeField', [], {}),
            'haut_page': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'lieu': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['localisations.Lieu']"}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organisateur': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['evenements.Organisateur']", 'symmetrical': 'False'}),
            'publish': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['evenements.TypeEvenement']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'url_reservation': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'evenements.festival': {
            'Meta': {'object_name': 'Festival', '_ormbases': ['evenements.Saison']},
            'saison_culture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['evenements.SaisonCulturelle']"}),
            'saison_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['evenements.Saison']", 'unique': 'True', 'primary_key': 'True'})
        },
        'evenements.organisateur': {
            'Meta': {'object_name': 'Organisateur'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rue': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'ville': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['localisations.Ville']"})
        },
        'evenements.prix': {
            'Meta': {'object_name': 'Prix'},
            'gratuit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'prix': ('django.db.models.fields.FloatField', [], {'blank': 'True'})
        },
        'evenements.saison': {
            'Meta': {'object_name': 'Saison'},
            'debut': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'fin': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        },
        'evenements.saisonculturelle': {
            'Meta': {'object_name': 'SaisonCulturelle', '_ormbases': ['evenements.Saison']},
            'saison_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['evenements.Saison']", 'unique': 'True', 'primary_key': 'True'})
        },
        'evenements.tarification': {
            'Meta': {'object_name': 'Tarification'},
            'evenement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['evenements.Evenement']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prix': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['evenements.Prix']", 'symmetrical': 'False'})
        },
        'evenements.typeevenement': {
            'Meta': {'object_name': 'TypeEvenement'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'localisations.lieu': {
            'Meta': {'object_name': 'Lieu'},
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

    complete_apps = ['evenements']