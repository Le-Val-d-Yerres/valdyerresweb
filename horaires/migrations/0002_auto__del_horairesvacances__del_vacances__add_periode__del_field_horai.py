# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'HorairesVacances'
        db.delete_table('horaires_horairesvacances')

        # Removing M2M table for field vacances on 'HorairesVacances'
        db.delete_table('horaires_horairesvacances_vacances')

        # Deleting model 'Vacances'
        db.delete_table('horaires_vacances')

        # Adding model 'Periode'
        db.create_table('horaires_periode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_debut', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('date_fin', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal('horaires', ['Periode'])

        # Deleting field 'Horaires.date_fin'
        db.delete_column('horaires_horaires', 'date_fin')

        # Deleting field 'Horaires.date_debut'
        db.delete_column('horaires_horaires', 'date_debut')

        # Adding M2M table for field periodes on 'Horaires'
        db.create_table('horaires_horaires_periodes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('horaires', models.ForeignKey(orm['horaires.horaires'], null=False)),
            ('periode', models.ForeignKey(orm['horaires.periode'], null=False))
        ))
        db.create_unique('horaires_horaires_periodes', ['horaires_id', 'periode_id'])


    def backwards(self, orm):
        # Adding model 'HorairesVacances'
        db.create_table('horaires_horairesvacances', (
            ('horaires_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['horaires.Horaires'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('horaires', ['HorairesVacances'])

        # Adding M2M table for field vacances on 'HorairesVacances'
        db.create_table('horaires_horairesvacances_vacances', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('horairesvacances', models.ForeignKey(orm['horaires.horairesvacances'], null=False)),
            ('vacances', models.ForeignKey(orm['horaires.vacances'], null=False))
        ))
        db.create_unique('horaires_horairesvacances_vacances', ['horairesvacances_id', 'vacances_id'])

        # Adding model 'Vacances'
        db.create_table('horaires_vacances', (
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_fin', self.gf('django.db.models.fields.DateField')()),
            ('date_debut', self.gf('django.db.models.fields.DateField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('horaires', ['Vacances'])

        # Deleting model 'Periode'
        db.delete_table('horaires_periode')

        # Adding field 'Horaires.date_fin'
        db.add_column('horaires_horaires', 'date_fin',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 10, 5, 0, 0)),
                      keep_default=False)

        # Adding field 'Horaires.date_debut'
        db.add_column('horaires_horaires', 'date_debut',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 10, 5, 0, 0)),
                      keep_default=False)

        # Removing M2M table for field periodes on 'Horaires'
        db.delete_table('horaires_horaires_periodes')


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
        'horaires.horaires': {
            'Meta': {'object_name': 'Horaires'},
            'dimanche_am_debut': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'dimanche_am_ferme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dimanche_am_fin': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'dimanche_journee_continue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dimanche_matin_debut': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'dimanche_matin_ferme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dimanche_matin_fin': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'equipement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['equipements.Equipement']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jeudi_am_debut': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'jeudi_am_ferme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'jeudi_am_fin': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'jeudi_journee_continue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'jeudi_matin_debut': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'jeudi_matin_ferme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'jeudi_matin_fin': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'lundi_am_debut': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'lundi_am_ferme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lundi_am_fin': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'lundi_journee_continue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lundi_matin_debut': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'lundi_matin_ferme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lundi_matin_fin': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'mardi_am_debut': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'mardi_am_ferme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mardi_am_fin': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'mardi_journee_continue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mardi_matin_debut': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'mardi_matin_ferme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mardi_matin_fin': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'mercredi_am_debut': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'mercredi_am_ferme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mercredi_am_fin': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'mercredi_journee_continue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mercredi_matin_debut': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'mercredi_matin_ferme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mercredi_matin_fin': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'periodes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['horaires.Periode']", 'symmetrical': 'False'}),
            'samedi_am_debut': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'samedi_am_ferme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'samedi_am_fin': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'samedi_journee_continue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'samedi_matin_debut': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'samedi_matin_ferme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'samedi_matin_fin': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'vendredi_am_debut': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'vendredi_am_ferme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vendredi_am_fin': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'vendredi_journee_continue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vendredi_matin_debut': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
            'vendredi_matin_ferme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vendredi_matin_fin': ('django.db.models.fields.TimeField', [], {'blank': 'True'})
        },
        'horaires.periode': {
            'Meta': {'object_name': 'Periode'},
            'date_debut': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'date_fin': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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

    complete_apps = ['horaires']