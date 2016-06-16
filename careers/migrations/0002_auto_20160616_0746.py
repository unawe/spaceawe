# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('careers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webinar',
            name='video_url',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
