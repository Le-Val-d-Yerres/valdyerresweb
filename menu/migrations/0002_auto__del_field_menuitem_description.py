# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'MenuItem.description'
        db.delete_column('menu_menuitem', 'description')


    def backwards(self, orm):
        # Adding field 'MenuItem.description'
        db.add_column('menu_menuitem', 'description',
                      self.gf('django.db.models.fields.TextField')(default=None),
                      keep_default=False)


    models = {
        'menu.menuitem': {
            'Meta': {'object_name': 'MenuItem'},
            'chemin': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.MenuItem']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['menu']