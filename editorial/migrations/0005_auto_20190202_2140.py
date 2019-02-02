# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-02 20:40
from __future__ import unicode_literals

from django.db import migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0004_auto_20170607_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagebase',
            name='image',
            field=filebrowser.fields.FileBrowseField(blank=True, default='', max_length=200, verbose_name="Image principale de l'article (facultatif)"),
            preserve_default=False,
        ),
    ]