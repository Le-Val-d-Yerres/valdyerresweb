# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localisations', '0001_initial'),
        ('evenements', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DateLieuEvenement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('debut', models.DateTimeField(verbose_name=b'Date de d\xc3\xa9but')),
                ('fin', models.DateTimeField(verbose_name=b'Date de fin')),
                ('evenement', models.ForeignKey(to='evenements.Evenement')),
                ('lieu', models.ForeignKey(to='localisations.Lieu')),
            ],
            options={
                'verbose_name': 'Date et Lieu',
                'verbose_name_plural': 'Dates et Lieux',
            },
            bases=(models.Model,),
        ),
    ]
