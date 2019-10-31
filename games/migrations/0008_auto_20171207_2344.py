# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0007_auto_20160303_1148'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameLinkTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(max_length=15, verbose_name='Language', db_index=True)),
                ('name', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'default_permissions': (),
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='gamelink',
            name='name',
        ),
        migrations.AddField(
            model_name='gamelinktranslation',
            name='master',
            field=models.ForeignKey(related_name='translations', to='games.GameLink', null=True),
        ),
    ]
