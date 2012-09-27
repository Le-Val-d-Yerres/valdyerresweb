# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EquipementFonction'
        db.create_table('equipements_equipementfonction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('pluriel', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('picto', self.gf('filebrowser.fields.FileBrowseField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('equipements', ['EquipementFonction'])

        # Adding model 'Equipement'
        db.create_table('equipements_equipement', (
            ('lieu_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['localisations.Lieu'], unique=True, primary_key=True)),
            ('fonction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['equipements.EquipementFonction'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254, blank=True)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('presentation', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('meta_description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('image', self.gf('filebrowser.fields.FileBrowseField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('equipements', ['Equipement'])

        # Adding model 'Facilite'
        db.create_table('equipements_facilite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('importance', self.gf('django.db.models.fields.IntegerField')()),
            ('picto', self.gf('filebrowser.fields.FileBrowseField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('equipements', ['Facilite'])

        # Adding model 'Facilites'
        db.create_table('equipements_facilites', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('equipement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['equipements.Equipement'])),
        ))
        db.send_create_signal('equipements', ['Facilites'])

        # Adding M2M table for field facilites on 'Facilites'
        db.create_table('equipements_facilites_facilites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('facilites', models.ForeignKey(orm['equipements.facilites'], null=False)),
            ('facilite', models.ForeignKey(orm['equipements.facilite'], null=False))
        ))
        db.create_unique('equipements_facilites_facilites', ['facilites_id', 'facilite_id'])


    def backwards(self, orm):
        # Deleting model 'EquipementFonction'
        db.delete_table('equipements_equipementfonction')

        # Deleting model 'Equipement'
        db.delete_table('equipements_equipement')

        # Deleting model 'Facilite'
        db.delete_table('equipements_facilite')

        # Deleting model 'Facilites'
        db.delete_table('equipements_facilites')

        # Removing M2M table for field facilites on 'Facilites'
        db.delete_table('equipements_facilites_facilites')


    models = {
        'equipements.equipement': {
            'Meta': {'object_name': 'Equipement', '_ormbases': ['localisations.Lieu']},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'fonction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['equipements.EquipementFonction']"}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'lieu_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['localisations.Lieu']", 'unique': 'True', 'primary_key': 'True'}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'presentation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'equipements.equipementfonction': {
            'Meta': {'object_name': 'EquipementFonction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'picto': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200'}),
            'pluriel': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        },
        'equipements.facilite': {
            'Meta': {'object_name': 'Facilite'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'importance': ('django.db.models.fields.IntegerField', [], {}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'picto': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        },
        'equipements.facilites': {
            'Meta': {'object_name': 'Facilites'},
            'equipement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['equipements.Equipement']"}),
            'facilites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['equipements.Facilite']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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

    complete_apps = ['equipements']