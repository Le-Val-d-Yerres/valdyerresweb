# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipements', '0002_equipement_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='TarifSpecifique',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('designation', models.CharField(max_length=255, verbose_name=b'D\xc3\xa9signation : (ex: "Entr\xc3\xa9e Adulte ")')),
                ('info_additionelle', models.CharField(max_length=255, null=True, verbose_name=b'Infos additionelles : (facultatif)', blank=True)),
                ('index', models.IntegerField(verbose_name=b"Ordre d'apparition (0 = en haut de liste)")),
                ('prix_residents', models.FloatField(verbose_name=b'Tarif r\xc3\xa9sidents ( 0 = gratuit  )')),
                ('prix_non_residents', models.FloatField(verbose_name=b'Tarif non r\xc3\xa9sidents ( 0 = gratuit  )')),
                ('categorie', models.ForeignKey(to='equipements.TarifCategorie')),
                ('equipement', models.ForeignKey(to='equipements.Equipement')),
            ],
            options={
                'ordering': ['categorie__index', 'index'],
                'verbose_name_plural': 'Tarifs',
            },
            bases=(models.Model,),
        ),
    ]
