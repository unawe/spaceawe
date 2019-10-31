from django.db import models
from django.core.urlresolvers import reverse
from django.conf import global_settings
from django.utils.translation import get_language_info
from django.utils.translation import ugettext as _
from ckeditor.fields import RichTextField
from sorl.thumbnail import ImageField
from parler.models import TranslatableModel, TranslatedFieldsModel
from parler.managers import TranslatableManager, TranslatableQuerySet
from select_multiple_field.models import SelectMultipleField

from django_ext.models import PublishingModel, PublishingManager
from django_ext.models.spaceawe import SpaceaweModel
from search.mixins import SearchModel


class GameQuerySet(TranslatableQuerySet):
    pass


class GameManager(PublishingManager, TranslatableManager):
    queryset_class = GameQuerySet


class Game(TranslatableModel, PublishingModel, SpaceaweModel, SearchModel):
    TYPE_CHOICES = (
        ('c', _('Citizen Science')),
        ('f', _('Fun Learning')),
        ('g', _('Game')),
        ('s', _('Software')),
        ('o', _('Other')),
    )
    PLATFORM_CHOICES = (
        ('f', _('Facebook')),
        ('w', _('Website')),
        ('s', _('Software')),
        ('a', _('App')),
        ('d', _('Data Collection')),
        ('o', _('Other')),
    )

    difficulty = models.IntegerField(default=0, verbose_name='difficulty level', help_text='From 1 to 5.', )
    fun = models.IntegerField(default=0, verbose_name='fun level', help_text='From 1 to 5.', )
    _game_type = SelectMultipleField(max_length=9999, choices=TYPE_CHOICES, db_column='game_type', )
    _languages = SelectMultipleField(max_length=9999, choices=global_settings.LANGUAGES, db_column='languages', )
    _platform = SelectMultipleField(max_length=9999, choices=PLATFORM_CHOICES, db_column='platform', )
    cover = ImageField(null=True, blank=True, upload_to='games')

    objects = GameManager()

    @property
    def main_visual(self):
        return self.cover.file if self.cover else None

    def links_list(self):
        return [link for link in self.links.all()]

    @property
    def game_type(self):
        decoder = dict(self.TYPE_CHOICES)
        decoded = [decoder[x] for x in self._game_type]
        return decoded

    @game_type.setter
    def game_type(self, value):
        self._game_type = value

    @property
    def languages(self):
        decoded = [get_language_info(x)['name'] for x in self._languages]
        return decoded

    @languages.setter
    def languages(self, value):
        self._languages = value

    @property
    def platform(self):
        decoder = dict(self.PLATFORM_CHOICES)
        decoded = [decoder[x] for x in self._platform]
        return decoded

    @platform.setter
    def platform(self, value):
        self._platform = value

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('games:detail', kwargs={'slug': self.slug, })

    class Meta:
        ordering = ['release_date']
        # verbose_name = 'game'


class GameTranslation(TranslatedFieldsModel):
    master = models.ForeignKey(Game, related_name='translations', null=True)
    title = models.CharField(blank=False, max_length=255, help_text='Short (and commonly used) name', )
    slug = models.SlugField(blank=False, max_length=255, help_text='The Slug must be unique, and closely match the title for better SEO; it is used as part of the URL.', )
    teaser = models.CharField(max_length=255, blank=True, )
    story = RichTextField(blank=True, null=True, config_name='default', help_text='Text to appear in Game page')

    class Meta:
        unique_together = (
            ('language_code', 'master'),
            ('language_code', 'title'),
            ('language_code', 'slug'),
        )
        # verbose_name = 'game translation'


class GameLink(TranslatableModel):
    game = models.ForeignKey(Game, related_name='links')
    url = models.URLField(max_length=255, verbose_name='URL')

    @property
    def caption(self):
        try:
            caption = self.name
        except GameLink.DoesNotExist:
            caption = self.url

        return caption

class GameLinkTranslation(TranslatedFieldsModel):
    master = models.ForeignKey(GameLink, related_name='translations', null=True)
    name = models.CharField(max_length=255, blank=True)


