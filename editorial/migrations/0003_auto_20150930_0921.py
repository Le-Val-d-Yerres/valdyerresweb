# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0002_newsletterbib'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletterbib',
            name='edito',
            field=models.TextField(verbose_name=b'Edito', blank=True),
            preserve_default=True,
        ),
    ]
