# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MenuItem'
        db.create_table('menu_menuitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('chemin', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('index', self.gf('django.db.models.fields.IntegerField')()),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menu.MenuItem'], null=True, blank=True)),
        ))
        db.send_create_signal('menu', ['MenuItem'])


    def backwards(self, orm):
        # Deleting model 'MenuItem'
        db.delete_table('menu_menuitem')


    models = {
        'menu.menuitem': {
            'Meta': {'object_name': 'MenuItem'},
            'chemin': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.MenuItem']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['menu']