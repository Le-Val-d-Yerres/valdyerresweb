# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Organisateur'
        db.create_table('evenements_organisateur', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('meta_description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('logo', self.gf('filebrowser.fields.FileBrowseField')(max_length=255, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255, blank=True)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('rue', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ville', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['localisations.Ville'])),
        ))
        db.send_create_signal('evenements', ['Organisateur'])

        # Adding model 'Saison'
        db.create_table('evenements_saison', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('debut', self.gf('django.db.models.fields.DateTimeField')()),
            ('fin', self.gf('django.db.models.fields.DateTimeField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('evenements', ['Saison'])

        # Adding model 'SaisonCulturelle'
        db.create_table('evenements_saisonculturelle', (
            ('saison_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['evenements.Saison'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('evenements', ['SaisonCulturelle'])

        # Adding model 'Festival'
        db.create_table('evenements_festival', (
            ('saison_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['evenements.Saison'], unique=True, primary_key=True)),
            ('saison_culture', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['evenements.SaisonCulturelle'])),
        ))
        db.send_create_signal('evenements', ['Festival'])

        # Adding model 'TypeEvenement'
        db.create_table('evenements_typeevenement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('evenements', ['TypeEvenement'])

        # Adding model 'Evenement'
        db.create_table('evenements_evenement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('meta_description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('debut', self.gf('django.db.models.fields.DateTimeField')()),
            ('fin', self.gf('django.db.models.fields.DateTimeField')()),
            ('image', self.gf('filebrowser.fields.FileBrowseField')(max_length=255, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('cadre_evenement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['evenements.Saison'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['evenements.TypeEvenement'])),
            ('lieu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['localisations.Lieu'])),
            ('publish', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('haut_page', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('evenements', ['Evenement'])

        # Adding M2M table for field organisateur on 'Evenement'
        db.create_table('evenements_evenement_organisateur', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('evenement', models.ForeignKey(orm['evenements.evenement'], null=False)),
            ('organisateur', models.ForeignKey(orm['evenements.organisateur'], null=False))
        ))
        db.create_unique('evenements_evenement_organisateur', ['evenement_id', 'organisateur_id'])

        # Adding model 'Prix'
        db.create_table('evenements_prix', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gratuit', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('prix', self.gf('django.db.models.fields.FloatField')(blank=True)),
        ))
        db.send_create_signal('evenements', ['Prix'])

        # Adding model 'Tarification'
        db.create_table('evenements_tarification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('evenement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['evenements.Evenement'])),
        ))
        db.send_create_signal('evenements', ['Tarification'])

        # Adding M2M table for field prix on 'Tarification'
        db.create_table('evenements_tarification_prix', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tarification', models.ForeignKey(orm['evenements.tarification'], null=False)),
            ('prix', models.ForeignKey(orm['evenements.prix'], null=False))
        ))
        db.create_unique('evenements_tarification_prix', ['tarification_id', 'prix_id'])


    def backwards(self, orm):
        # Deleting model 'Organisateur'
        db.delete_table('evenements_organisateur')

        # Deleting model 'Saison'
        db.delete_table('evenements_saison')

        # Deleting model 'SaisonCulturelle'
        db.delete_table('evenements_saisonculturelle')

        # Deleting model 'Festival'
        db.delete_table('evenements_festival')

        # Deleting model 'TypeEvenement'
        db.delete_table('evenements_typeevenement')

        # Deleting model 'Evenement'
        db.delete_table('evenements_evenement')

        # Removing M2M table for field organisateur on 'Evenement'
        db.delete_table('evenements_evenement_organisateur')

        # Deleting model 'Prix'
        db.delete_table('evenements_prix')

        # Deleting model 'Tarification'
        db.delete_table('evenements_tarification')

        # Removing M2M table for field prix on 'Tarification'
        db.delete_table('evenements_tarification_prix')


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
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
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