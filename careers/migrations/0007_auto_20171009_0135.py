# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('careers', '0006_booklet__languages'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='booklettranslation',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='booklettranslation',
            name='master',
        ),
        migrations.DeleteModel(
            name='Booklet',
        ),
        migrations.DeleteModel(
            name='BookletTranslation',
        ),
    ]
