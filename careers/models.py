import os

from django.db import models
from django.conf import global_settings
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import get_language_info
from django.utils.translation import ugettext as _

from activities.models import MetadataOption, utils

from ckeditor.fields import RichTextField
from sorl.thumbnail import ImageField
from parler.models import TranslatableModel, TranslatedFieldsModel
from parler.managers import TranslatableManager, TranslatableQuerySet
from select_multiple_field.models import SelectMultipleField

from django_ext.models import PublishingModel, PublishingManager, BaseAttachmentModel
from django_ext.models.spaceawe import SpaceaweModel
from search.mixins import SearchModel

import logging


class CareerQuerySet(TranslatableQuerySet):
    pass


class CareerManager(PublishingManager, TranslatableManager):
    queryset_class = CareerQuerySet


class Career(TranslatableModel, PublishingModel, SpaceaweModel, SearchModel):
    cover = ImageField(null=True, blank=True, upload_to='careers')
    _languages = SelectMultipleField(max_length=9999, choices=global_settings.LANGUAGES, db_column='languages')

    objects = CareerManager()

    @property
    def main_visual(self):
        return self.cover.file if self.cover else None

    def links_list(self):
        return [link for link in self.links.all()]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('careers:career-detail', kwargs={'slug': self.slug, })

    def zip_url(self):
        return self.download_url('zip')

    def pdf_url(self):
        return self.download_url('pdf')

    def epub_url(self):
        return self.download_url('epub')

    def rtf_url(self):
        return self.download_url('rtf')

    def download_url(self, resource):
        return os.path.join(settings.MEDIA_URL, self.media_key(), 'download', self.download_key() + '.' + resource)
    def download_path(self, resource):
        return os.path.join(settings.MEDIA_ROOT, self.media_key(), 'download', self.download_key() + '.' + resource)

    def attachment_url(self, filename):
        if filename.startswith('http') or filename.startswith('/'):
            result = filename
        else:
            result = os.path.join(settings.MEDIA_URL, 'activities/attach', self.uuid, filename)
        return result

    def download_key(self):
        return self.slug + '-careers-' + str(self.pk)

    @classmethod
    def media_key(cls):
        return str(cls._meta.verbose_name_plural)

    class Meta:
        ordering = ['release_date']


class CareerTranslation(TranslatedFieldsModel):
    master = models.ForeignKey(Career, related_name='translations', null=True)
    title = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    teaser = models.CharField(max_length=255, blank=True)
    story = RichTextField(blank=True, null=True, config_name='default')
    field = models.CharField(max_length=255, blank=True)
    career_type = models.CharField(max_length=255, blank=True)
    level_of_study = models.CharField(max_length=255, blank=True)
    # interview = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = (
            ('language_code', 'master'),
            ('language_code', 'title'),
            ('language_code', 'slug'),
        )


class InterviewQuerySet(TranslatableQuerySet):
    pass


class InterviewManager(PublishingManager, TranslatableManager):
    queryset_class = InterviewQuerySet


class Interview(TranslatableModel, PublishingModel, SpaceaweModel, SearchModel):
    video_url = models.URLField(max_length=255, null=True, blank=True)
    cover = ImageField(null=True, blank=True, upload_to='interviews')
    _languages = SelectMultipleField(max_length=9999, choices=global_settings.LANGUAGES, db_column='languages')
    career = models.ManyToManyField(Career)

    objects = InterviewManager()

    @property
    def main_visual(self):
        return self.cover.file if self.cover else None

    def question_list(self):
        return [question for question in self.questions.all()]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('careers:interview-detail', kwargs={'slug': self.slug, })

    @classmethod
    def media_key(cls):
        return str(cls._meta.verbose_name_plural)

    def zip_url(self):
        return self.download_url('zip')

    def pdf_url(self):
        return self.download_url('pdf')

    def epub_url(self):
        return self.download_url('epub')

    def rtf_url(self):
        return self.download_url('rtf')

    def download_url(self, resource):
        return os.path.join(settings.MEDIA_URL, self.media_key(), 'download', self.download_key() + '.' + resource)
    def download_path(self, resource):
        return os.path.join(settings.MEDIA_ROOT, self.media_key(), 'download', self.download_key() + '.' + resource)

    def attachment_url(self, filename):
        if filename.startswith('http') or filename.startswith('/'):
            result = filename
        else:
            result = os.path.join(settings.MEDIA_URL, 'activities/attach', self.uuid, filename)
        return result

    def download_key(self):
        return self.slug + '-interviews-' + str(self.pk)

    class Meta:
        ordering = ['release_date']


class InterviewTranslation(TranslatedFieldsModel):
    master = models.ForeignKey(Interview, related_name='translations', null=True)
    title = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    teaser = models.CharField(max_length=255, blank=True)
    story = RichTextField(blank=True, null=True, config_name='default')
    name = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    place_of_job = models.CharField(max_length=255, blank=True)
    profession = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = (
            ('language_code', 'master'),
            ('language_code', 'title'),
            ('language_code', 'slug'),
        )


class InterviewQuestion(models.Model):
    interview = models.ForeignKey(Interview, related_name='questions')
    question_text = models.CharField(max_length=255, blank=True)
    video_url = models.URLField(max_length=255)  # Maybe not good idea
    image = ImageField(null=True, blank=True, upload_to='interviews')

    @property
    def main_visual(self):
        return self.image.file if self.image else None

    def caption(self):
        return self.question_text if self.question_text else self.video_url

    def __str__(self):
        return self.question_text


class WebinarQuerySet(TranslatableQuerySet):
    pass


class WebinarManager(PublishingManager, TranslatableManager):
    queryset_class = WebinarQuerySet


class Webinar(TranslatableModel, PublishingModel, SpaceaweModel, SearchModel):
    video_url = models.URLField(max_length=255, blank=True, null=True)
    cover = ImageField(null=True, blank=True, upload_to='webinars')
    _languages = SelectMultipleField(max_length=9999, choices=global_settings.LANGUAGES, db_column='languages')

    objects = WebinarManager()

    @property
    def main_visual(self):
        return self.cover.file if self.cover else None

    def links_list(self):
        return [link for link in self.links.all()]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('careers:webinar-detail', kwargs={'slug': self.slug, })

    @classmethod
    def media_key(cls):
        return str(cls._meta.verbose_name_plural)

    def zip_url(self):
        return self.download_url('zip')

    def pdf_url(self):
        return self.download_url('pdf')

    def epub_url(self):
        return self.download_url('epub')

    def rtf_url(self):
        return self.download_url('rtf')

    def download_url(self, resource):
        return os.path.join(settings.MEDIA_URL, self.media_key(), 'download', self.download_key() + '.' + resource)
    def download_path(self, resource):
        return os.path.join(settings.MEDIA_ROOT, self.media_key(), 'download', self.download_key() + '.' + resource)

    def attachment_url(self, filename):
        if filename.startswith('http') or filename.startswith('/'):
            result = filename
        else:
            result = os.path.join(settings.MEDIA_URL, 'activities/attach', self.uuid, filename)
        return result

    def download_key(self):
        return self.slug + '-interviews-' + str(self.pk)

    class Meta:
        ordering = ['release_date']


class WebinarTranslation(TranslatedFieldsModel):
    master = models.ForeignKey(Webinar, related_name='translations', null=True)
    title = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    teaser = models.CharField(max_length=255, blank=True)
    story = RichTextField(blank=True, null=True, config_name='default')
    register = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    target_group = models.CharField(max_length=255, blank=True)
    language = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = (
            ('language_code', 'master'),
            ('language_code', 'title'),
            ('language_code', 'slug'),
        )


class TeachingMaterialQuerySet(TranslatableQuerySet):
    pass


class TeachingMaterialManager(PublishingManager, TranslatableManager):
    queryset_class = TeachingMaterialQuerySet


class TeachingMaterial(TranslatableModel, PublishingModel, SpaceaweModel):
    activity_type_choises = (
        ('g', 'Game'),
        ('l', 'Lesson plan')
    )
    cover = ImageField(null=True, blank=True, upload_to='careers/teaching-materials/covers')
    age = models.ManyToManyField(MetadataOption, limit_choices_to={'group': 'age'}, related_name='age+', )
    learning = models.CharField(max_length=2, choices=activity_type_choises, blank=False, null=False, verbose_name='type of learning activity', )
    _languages = SelectMultipleField(max_length=9999, choices=global_settings.LANGUAGES, db_column='languages')

    objects = TeachingMaterialManager()

    def age_range(self):
        # return ' '.join(obj.title for obj in self.age.all())
        age_ranges = [obj.title for obj in self.age.all()]
        return utils.beautify_age_range(age_ranges)

    @property
    def main_visual(self):
        return self.cover.file if self.cover else None

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('careers:teaching-material-detail', kwargs={'slug': self.slug, })

    def attachment_url(self, filename):
        if filename.startswith('http') or filename.startswith('/'):
            result = filename
        else:
            result = os.path.join(settings.MEDIA_URL, 'careers/teaching-materials/attachments', self.id, filename)
        return result

    @classmethod
    def media_key(cls):
        return str(cls._meta.verbose_name_plural)

    class Meta:
        ordering = ['release_date']


class TeachingMaterialTranslation(TranslatedFieldsModel):
    master = models.ForeignKey(TeachingMaterial, related_name='translations', null=True)
    title = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    story = RichTextField(blank=True, null=True, config_name='smartpages')
    language = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = (
            ('language_code', 'master'),
            ('language_code', 'title'),
            ('language_code', 'slug'),
        )


def get_file_path_step(instance, filename):
    return os.path.join('careers/teaching-materials/attachments', str(instance.hostmodel.id), filename)


class TeachingMaterialAttachment(BaseAttachmentModel):
    hostmodel = models.ForeignKey(TeachingMaterial, related_name='attachments')
    file = models.FileField(null=True, blank=True, upload_to=get_file_path_step)


class BookletQuerySet(TranslatableQuerySet):
    pass


class BookletManager(PublishingManager, TranslatableManager):
    queryset_class = BookletQuerySet


class Booklet(TranslatableModel, PublishingModel):
    _languages = SelectMultipleField(max_length=9999, choices=global_settings.LANGUAGES, db_column='languages')
    objects = BookletManager()

    @property
    def main_visual(self):
        return self.cover.file if self.cover else None

    def __str__(self):
        return self.title

    def pdf_url(self):
        return self.download_url('pdf')

    def download_url(self, resource):
        return os.path.join(settings.MEDIA_URL, self.media_key(), 'download', self.download_key() + '.' + resource)

    def download_path(self, resource):
        return os.path.join(settings.MEDIA_ROOT, self.media_key(), 'download', self.download_key() + '.' + resource)

    def download_key(self):
        return self.slug + '-booklet-' + str(self.pk)

    @classmethod
    def media_key(cls):
        return str(cls._meta.verbose_name_plural)

    class Meta:
        ordering = ['release_date']


class BookletTranslation(TranslatedFieldsModel):
    master = models.ForeignKey(Booklet, related_name='translations', null=True)
    title = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    teaser = models.CharField(max_length=255, blank=True)
    story = RichTextField(blank=True, null=True, config_name='default')
    booklet = models.FileField(null=False, blank=False, upload_to='booklets/files')
    cover = ImageField(null=True, blank=True, upload_to='booklets/covers')

    class Meta:
        unique_together = (
            ('language_code', 'master'),
            ('language_code', 'title'),
            ('language_code', 'slug'),
        )