# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('careers', '0009_auto_20180128_0214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='video_url',
            field=models.URLField(max_length=255, blank=True, null=True),
        ),
    ]
