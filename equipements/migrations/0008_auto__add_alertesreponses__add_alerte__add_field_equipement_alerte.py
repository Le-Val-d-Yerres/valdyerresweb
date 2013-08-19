# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AlertesReponses'
        db.create_table('equipements_alertesreponses', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('alerte', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['equipements.Alerte'])),
            ('equipement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['equipements.Equipement'])),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('prenom', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('rue', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('codePostal', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('ville', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('tel', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('mail', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('etat', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('equipements', ['AlertesReponses'])

        # Adding model 'Alerte'
        db.create_table('equipements_alerte', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('texte_lien', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('equipements', ['Alerte'])

        # Adding M2M table for field users on 'Alerte'
        db.create_table('equipements_alerte_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('alerte', models.ForeignKey(orm['equipements.alerte'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('equipements_alerte_users', ['alerte_id', 'user_id'])

        # Adding field 'Equipement.alerte'
        db.add_column('equipements_equipement', 'alerte',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['equipements.Alerte'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'AlertesReponses'
        db.delete_table('equipements_alertesreponses')

        # Deleting model 'Alerte'
        db.delete_table('equipements_alerte')

        # Removing M2M table for field users on 'Alerte'
        db.delete_table('equipements_alerte_users')

        # Deleting field 'Equipement.alerte'
        db.delete_column('equipements_equipement', 'alerte_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'equipements.alerte': {
            'Meta': {'object_name': 'Alerte'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'texte_lien': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'})
        },
        'equipements.alertesreponses': {
            'Meta': {'ordering': "['etat', '-date']", 'object_name': 'AlertesReponses'},
            'alerte': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['equipements.Alerte']"}),
            'codePostal': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'equipement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['equipements.Equipement']"}),
            'etat': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'prenom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rue': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ville': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'equipements.equipement': {
            'Meta': {'ordering': "('fonction__nom', 'ville__nom')", 'object_name': 'Equipement', '_ormbases': ['localisations.Lieu']},
            'alerte': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['equipements.Alerte']", 'null': 'True'}),
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