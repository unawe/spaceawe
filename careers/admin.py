from django.contrib import admin
from django import forms
from parler.admin import TranslatableAdmin, TranslatableModelForm

from .models import Interview, InterviewQuestion, Career, Webinar

class InterviewQuestionInlineAdmin(admin.TabularInline):
    model = InterviewQuestion
    fields = ('question_text', 'video_url', )
    extra = 1


class InterviewAdminForm(TranslatableModelForm):

    class Meta:
        model = Interview
        fields = ('title', 'slug', 'release_date', 'published', 'featured', 'cover', 'teaser', 'story', '_languages', 'video_url', 'name', 'country', 'place_of_job', )


@admin.register(Interview)
class InterviewAdmin(TranslatableAdmin):
    list_display = ('title', 'all_languages_column', )

    fieldsets = (
        (None,
         {'fields': ('title', 'slug', 'teaser', 'cover', 'video_url', ), }),
        ('Space Awareness Category',
         {'fields': (('space', 'earth', 'navigation', 'heritage', ), )}),
        (None,
         {'fields': (('_languages', ),
                     ('name', 'country', 'place_of_job', ), )}),
        ('Publishing',
         {'fields': (('release_date', ),
                     ('published', 'featured', ),) }),
        (None,
         {'fields': ('story', ), }),
    )

    def get_prepopulated_fields(self, request, obj=None):
        return {
            'slug': ('title',),
        }

    inlines = (
        InterviewQuestionInlineAdmin,
    )


class CareerAdminForm(TranslatableModelForm):

    class Meta:
        model = Career
        fields = ('title', 'slug', 'release_date', 'published', 'featured', 'cover', 'teaser', 'story', '_languages', 'field', 'career_type', 'level_of_study', 'interview', )


@admin.register(Career)
class CareerAdmin(TranslatableAdmin):
    list_display = ('title', 'all_languages_column', )

    fieldsets = (
        (None,
         {'fields': ('title', 'slug', 'teaser', 'cover', ), }),
        ('Space Awareness Category',
         {'fields': (('space', 'earth', 'navigation', 'heritage', ), )}),
        (None,
         {'fields': (('_languages', ),
                     ('field', 'career_type', 'level_of_study', 'interview', ), )}),
        ('Publishing',
         {'fields': (('release_date', ),
                     ('published', 'featured', ),) }),
        (None,
         {'fields': ('story', ), }),
    )

    def get_prepopulated_fields(self, request, obj=None):
        return {
            'slug': ('title',),
        }


class WebinarAdminForm(TranslatableModelForm):

    class Meta:
        model = Webinar
        fields = ('title', 'slug', 'release_date', 'published', 'featured', 'cover', 'teaser', 'story', '_languages', 'video_url', 'register', 'location', 'target_group', 'language', )


@admin.register(Webinar)
class CareerAdmin(TranslatableAdmin):
    list_display = ('title', 'all_languages_column', )

    fieldsets = (
        (None,
         {'fields': ('title', 'slug', 'teaser', 'cover', ), }),
        ('Space Awareness Category',
         {'fields': (('space', 'earth', 'navigation', 'heritage', ), )}),
        (None,
         {'fields': (('_languages', ),
                     ('video_url', 'register', 'location', 'target_group', 'language', ), )}),
        ('Publishing',
         {'fields': (('release_date', ),
                     ('published', 'featured', ),) }),
        (None,
         {'fields': ('story', ), }),
    )

    def get_prepopulated_fields(self, request, obj=None):
        return {
            'slug': ('title',),
        }
