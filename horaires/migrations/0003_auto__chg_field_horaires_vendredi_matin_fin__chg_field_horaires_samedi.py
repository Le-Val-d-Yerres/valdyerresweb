# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Horaires.vendredi_matin_fin'
        db.alter_column('horaires_horaires', 'vendredi_matin_fin', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Horaires.samedi_matin_fin'
        db.alter_column('horaires_horaires', 'samedi_matin_fin', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Horaires.samedi_matin_debut'
        db.alter_column('horaires_horaires', 'samedi_matin_debut', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Horaires.mardi_matin_debut'
        db.alter_column('horaires_horaires', 'mardi_matin_debut', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Horaires.samedi_am_debut'
        db.alter_column('horaires_horaires', 'samedi_am_debut', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Horaires.mercredi_am_debut'
        db.alter_column('horaires_horaires', 'mercredi_am_debut', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Horaires.mercredi_matin_debut'
        db.alter_column('horaires_horaires', 'mercredi_matin_debut', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Horaires.dimanche_matin_debut'
        db.alter_column('horaires_horaires', 'dimanche_matin_debut', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Horaires.mardi_matin_fin'
        db.alter_column('horaires_horaires', 'mardi_matin_fin', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Horaires.lundi_am_fin'
        db.alter_column('horaires_horaires', 'lundi_am_fin', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Horaires.lundi_matin_debut'
        db.alter_column('horaires_horaires', 'lundi_matin_debut', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Horaires.vendredi_am_fin'
        db.alter_column('horaires_horaires', 'vendredi_am_fin', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Horaires.samedi_am_fin'
        db.alter_column('horaires_horaires', 'samedi_am_fin', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Horaires.mercredi_am_fin'
        db.alter_column('horaires_horaires', 'mercredi_am_fin', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Horaires.jeudi_matin_fin'
        db.alter_column('horaires_horaires', 'jeudi_matin_fin', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Horaires.jeudi_am_fin'
        db.alter_column('horaires_horaires', 'jeudi_am_fin', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Horaires.mardi_am_fin'
        db.alter_column('horaires_horaires', 'mardi_am_fin', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Horaires.jeudi_am_debut'
        db.alter_column('horaires_horaires', 'jeudi_am_debut', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Horaires.lundi_am_debut'
        db.alter_column('horaires_horaires', 'lundi_am_debut', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Horaires.vendredi_matin_debut'
        db.alter_column('horaires_horaires', 'vendredi_matin_debut', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Horaires.mardi_am_debut'
        db.alter_column('horaires_horaires', 'mardi_am_debut', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Horaires.dimanche_matin_fin'
        db.alter_column('horaires_horaires', 'dimanche_matin_fin', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Horaires.jeudi_matin_debut'
        db.alter_column('horaires_horaires', 'jeudi_matin_debut', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Horaires.dimanche_am_fin'
        db.alter_column('horaires_horaires', 'dimanche_am_fin', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Horaires.lundi_matin_fin'
        db.alter_column('horaires_horaires', 'lundi_matin_fin', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Horaires.vendredi_am_debut'
        db.alter_column('horaires_horaires', 'vendredi_am_debut', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Horaires.dimanche_am_debut'
        db.alter_column('horaires_horaires', 'dimanche_am_debut', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Horaires.mercredi_matin_fin'
        db.alter_column('horaires_horaires', 'mercredi_matin_fin', self.gf('django.db.models.fields.TimeField')(null=True))

    def backwards(self, orm):

        # Changing field 'Horaires.vendredi_matin_fin'
        db.alter_column('horaires_horaires', 'vendredi_matin_fin', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)))

        # Changing field 'Horaires.samedi_matin_fin'
        db.alter_column('horaires_horaires', 'samedi_matin_fin', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)))

        # Changing field 'Horaires.samedi_matin_debut'
        db.alter_column('horaires_horaires', 'samedi_matin_debut', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)))

        # Changing field 'Horaires.mardi_matin_debut'
        db.alter_column('horaires_horaires', 'mardi_matin_debut', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)))

        # Changing field 'Horaires.samedi_am_debut'
        db.alter_column('horaires_horaires', 'samedi_am_debut', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)))

        # Changing field 'Horaires.mercredi_am_debut'
        db.alter_column('horaires_horaires', 'mercredi_am_debut', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)))

        # Changing field 'Horaires.mercredi_matin_debut'
        db.alter_column('horaires_horaires', 'mercredi_matin_debut', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)))

        # Changing field 'Horaires.dimanche_matin_debut'
        db.alter_column('horaires_horaires', 'dimanche_matin_debut', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)))

        # Changing field 'Horaires.mardi_matin_fin'
        db.alter_column('horaires_horaires', 'mardi_matin_fin', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)))

        # Changing field 'Horaires.lundi_am_fin'
        db.alter_column('horaires_horaires', 'lundi_am_fin', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)))

        # Changing field 'Horaires.lundi_matin_debut'
        db.alter_column('horaires_horaires', 'lundi_matin_debut', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)))

        # Changing field 'Horaires.vendredi_am_fin'
        db.alter_column('horaires_horaires', 'vendredi_am_fin', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)))

        # Changing field 'Horaires.samedi_am_fin'
        db.alter_column('horaires_horaires', 'samedi_am_fin', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)))

        # Changing field 'Horaires.mercredi_am_fin'
        db.alter_column('horaires_horaires', 'mercredi_am_fin', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)))

        # Changing field 'Horaires.jeudi_matin_fin'
        db.alter_column('horaires_horaires', 'jeudi_matin_fin', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)))

        # Changing field 'Horaires.jeudi_am_fin'
        db.alter_column('horaires_horaires', 'jeudi_am_fin', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)))

        # Changing field 'Horaires.mardi_am_fin'
        db.alter_column('horaires_horaires', 'mardi_am_fin', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)))

        # Changing field 'Horaires.jeudi_am_debut'
        db.alter_column('horaires_horaires', 'jeudi_am_debut', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)))

        # Changing field 'Horaires.lundi_am_debut'
        db.alter_column('horaires_horaires', 'lundi_am_debut', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)))

        # Changing field 'Horaires.vendredi_matin_debut'
        db.alter_column('horaires_horaires', 'vendredi_matin_debut', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)))

        # Changing field 'Horaires.mardi_am_debut'
        db.alter_column('horaires_horaires', 'mardi_am_debut', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)))

        # Changing field 'Horaires.dimanche_matin_fin'
        db.alter_column('horaires_horaires', 'dimanche_matin_fin', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)))

        # Changing field 'Horaires.jeudi_matin_debut'
        db.alter_column('horaires_horaires', 'jeudi_matin_debut', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)))

        # Changing field 'Horaires.dimanche_am_fin'
        db.alter_column('horaires_horaires', 'dimanche_am_fin', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)))

        # Changing field 'Horaires.lundi_matin_fin'
        db.alter_column('horaires_horaires', 'lundi_matin_fin', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)))

        # Changing field 'Horaires.vendredi_am_debut'
        db.alter_column('horaires_horaires', 'vendredi_am_debut', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)))

        # Changing field 'Horaires.dimanche_am_debut'
        db.alter_column('horaires_horaires', 'dimanche_am_debut', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)))

        # Changing field 'Horaires.mercredi_matin_fin'
        db.alter_column('horaires_horaires', 'mercredi_matin_fin', self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 10, 8, 0, 0)))

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
            'dimanche_am_debut': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'dimanche_am_ferme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dimanche_am_fin': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'dimanche_journee_continue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dimanche_matin_debut': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'dimanche_matin_ferme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dimanche_matin_fin': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'equipement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['equipements.Equipement']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jeudi_am_debut': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'jeudi_am_ferme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'jeudi_am_fin': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'jeudi_journee_continue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'jeudi_matin_debut': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'jeudi_matin_ferme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'jeudi_matin_fin': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'lundi_am_debut': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'lundi_am_ferme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lundi_am_fin': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'lundi_journee_continue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lundi_matin_debut': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'lundi_matin_ferme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lundi_matin_fin': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'mardi_am_debut': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'mardi_am_ferme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mardi_am_fin': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'mardi_journee_continue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mardi_matin_debut': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'mardi_matin_ferme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mardi_matin_fin': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'mercredi_am_debut': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'mercredi_am_ferme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mercredi_am_fin': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'mercredi_journee_continue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mercredi_matin_debut': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'mercredi_matin_ferme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mercredi_matin_fin': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'periodes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['horaires.Periode']", 'symmetrical': 'False'}),
            'samedi_am_debut': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'samedi_am_ferme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'samedi_am_fin': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'samedi_journee_continue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'samedi_matin_debut': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'samedi_matin_ferme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'samedi_matin_fin': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'vendredi_am_debut': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'vendredi_am_ferme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vendredi_am_fin': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'vendredi_journee_continue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vendredi_matin_debut': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'vendredi_matin_ferme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vendredi_matin_fin': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'})
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