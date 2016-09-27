# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evenements', '0004_auto_20151106_1139'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='saisonculturelle',
            options={'ordering': ['-debut']},
        ),
    ]
