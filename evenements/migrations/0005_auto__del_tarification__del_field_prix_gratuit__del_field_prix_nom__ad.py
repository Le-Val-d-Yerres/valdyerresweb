# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Tarification'
        db.delete_table('evenements_tarification')

        # Removing M2M table for field prix on 'Tarification'
        db.delete_table('evenements_tarification_prix')

        # Deleting field 'Prix.gratuit'
        db.delete_column('evenements_prix', 'gratuit')

        # Deleting field 'Prix.nom'
        db.delete_column('evenements_prix', 'nom')

        # Adding field 'Prix.intitule'
        db.add_column('evenements_prix', 'intitule',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=255),
                      keep_default=False)

        # Adding field 'Prix.evenement'
        db.add_column('evenements_prix', 'evenement',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['evenements.Evenement']),
                      keep_default=False)


        # Changing field 'Prix.prix'
        db.alter_column('evenements_prix', 'prix', self.gf('django.db.models.fields.FloatField')(null=True))

    def backwards(self, orm):
        # Adding model 'Tarification'
        db.create_table('evenements_tarification', (
            ('evenement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['evenements.Evenement'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('evenements', ['Tarification'])

        # Adding M2M table for field prix on 'Tarification'
        db.create_table('evenements_tarification_prix', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tarification', models.ForeignKey(orm['evenements.tarification'], null=False)),
            ('prix', models.ForeignKey(orm['evenements.prix'], null=False))
        ))
        db.create_unique('evenements_tarification_prix', ['tarification_id', 'prix_id'])

        # Adding field 'Prix.gratuit'
        db.add_column('evenements_prix', 'gratuit',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Prix.nom'
        db.add_column('evenements_prix', 'nom',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=255),
                      keep_default=False)

        # Deleting field 'Prix.intitule'
        db.delete_column('evenements_prix', 'intitule')

        # Deleting field 'Prix.evenement'
        db.delete_column('evenements_prix', 'evenement_id')


        # Changing field 'Prix.prix'
        db.alter_column('evenements_prix', 'prix', self.gf('django.db.models.fields.FloatField')(default=None))

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
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'equipements.equipementfonction': {
            'Meta': {'object_name': 'EquipementFonction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'picto': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200'}),
            'pluriel': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        },
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
            'Meta': {'ordering': "['ville__nom']", 'object_name': 'Organisateur'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'orga_equipement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['equipements.Equipement']", 'null': 'True', 'blank': 'True'}),
            'orga_service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['services.Service']", 'null': 'True', 'blank': 'True'}),
            'orga_ville': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'orga_orga_ville'", 'null': 'True', 'to': "orm['localisations.Ville']"}),
            'rue': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'ville': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['localisations.Ville']"})
        },
        'evenements.prix': {
            'Meta': {'object_name': 'Prix'},
            'evenement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['evenements.Evenement']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intitule': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'prix': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'})
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
        'evenements.typeevenement': {
            'Meta': {'object_name': 'TypeEvenement'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
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

    complete_apps = ['evenements']