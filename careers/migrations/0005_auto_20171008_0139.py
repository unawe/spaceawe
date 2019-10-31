# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('careers', '0004_auto_20170525_2245'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booklet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('featured', models.BooleanField(default=False)),
                ('published', models.BooleanField(default=True)),
                ('release_date', models.DateTimeField()),
                ('embargo_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ['release_date'],
            },
        ),
        migrations.CreateModel(
            name='BookletTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('language_code', models.CharField(verbose_name='Language', max_length=15, db_index=True)),
                ('title', models.CharField(max_length=255, blank=True)),
                ('slug', models.SlugField(max_length=255, blank=True)),
                ('teaser', models.CharField(max_length=255, blank=True)),
                ('story', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('booklet', models.FileField(upload_to='booklets/files')),
                ('cover', sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to='booklets/covers')),
                ('master', models.ForeignKey(null=True, related_name='translations', to='careers.Booklet')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='booklettranslation',
            unique_together=set([('language_code', 'slug'), ('language_code', 'master'), ('language_code', 'title')]),
        ),
    ]
