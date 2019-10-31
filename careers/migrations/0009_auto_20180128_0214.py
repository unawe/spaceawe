# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('careers', '0008_auto_20171009_0138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='video_url',
            field=models.URLField(max_length=255, null=True),
        ),
    ]
