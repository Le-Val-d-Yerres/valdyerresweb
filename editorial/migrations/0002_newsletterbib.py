# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipements', '0002_equipement_type'),
        ('editorial', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsletterBib',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('maj', models.DateField(auto_now=True, verbose_name=b'Date de mise \xc3\xa0 jour', auto_now_add=True)),
                ('edito', models.TextField(verbose_name=b'Edito')),
                ('evenement_debut', models.DateField(verbose_name=b'Date de D\xc3\xa9but des \xc3\xa9v\xc3\xa9nements')),
                ('evenement_fin', models.DateField(verbose_name=b'Date de fin des \xc3\xa9v\xc3\xa9nements')),
                ('bib', models.ForeignKey(to='equipements.Equipement')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
