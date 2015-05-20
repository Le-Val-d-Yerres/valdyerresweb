# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=255)),
                ('chemin', models.CharField(max_length=255)),
                ('index', models.IntegerField()),
                ('parent', models.ForeignKey(blank=True, to='menu.MenuItem', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
