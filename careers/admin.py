from django.contrib import admin
from django import forms
from parler.admin import TranslatableAdmin, TranslatableModelForm

from .models import Interview, InterviewQuestion, Career, Webinar, TeachingMaterial, TeachingMaterialAttachment, Booklet


class InterviewQuestionInlineAdmin(admin.TabularInline):
    model = InterviewQuestion
    fields = ('question_text', 'video_url', 'image', )
    extra = 1


class InterviewAdminForm(TranslatableModelForm):

    def clean(self):
        cleaned_data = super().clean()

        video_url = cleaned_data.get('video_url', None)
        cover = cleaned_data.get('cover', None)

        if not video_url and not cover:
            raise forms.ValidationError(
                "Please fill video URL or cover image."
            )

    class Meta:
        model = Interview
        fields = ('title', 'slug', 'release_date', 'published', 'featured', 'cover', 'teaser', 'story', 'career',
                  '_languages', 'video_url', 'name', 'country', 'place_of_job', 'career',)


@admin.register(Interview)
class InterviewAdmin(TranslatableAdmin):
    list_display = ('title', 'all_languages_column', )
    form = InterviewAdminForm
    fieldsets = (
        (None,
         {'fields': ('title', 'slug', 'teaser', 'cover', 'video_url', ), }),
        ('Space Awareness Category',
         {'fields': (('space', 'earth', 'navigation', 'heritage', ), )}),
        (None,
         {'fields': (('_languages', ),
                     ('name', 'country', 'place_of_job', 'profession', 'career',), )}),
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
        fields = ('title', 'slug', 'release_date', 'published', 'featured', 'cover', 'teaser', 'story',
                  '_languages', 'field', 'career_type', 'level_of_study', )


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
                     ('field', 'career_type', 'level_of_study', ), )}),
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


class TeachingMaterialAdminForm(TranslatableModelForm):

    class Meta:
        model = TeachingMaterial
        fields = ('title', 'slug', 'release_date', 'published', 'featured', 'cover', 'story', )


class TeachingMaterialAttachmentInline(admin.TabularInline):
    model = TeachingMaterialAttachment
    fields = ('title', 'file', 'position', 'show')
    min_num = 2
    extra = 1


@admin.register(TeachingMaterial)
class TeachingMaterialAdmin(TranslatableAdmin):
    list_display = ('title', 'all_languages_column', )

    fieldsets = (
        (None,
         {'fields': ('title', 'slug', 'cover', ), }),
        ('Space Awareness Category',
         {'fields': (('space', 'earth', 'navigation', 'heritage', ), )}),
        (None,
         {'fields': (('_languages', ),
                     ('age', 'learning', ), )}),
        ('Publishing',
         {'fields': (('release_date', ),
                     ('published', 'featured', ),) }),
        (None,
         {'fields': ('story', ), }),
    )

    inlines = (
        TeachingMaterialAttachmentInline,
    )

    def get_prepopulated_fields(self, request, obj=None):
        return {
            'slug': ('title',),
        }


@admin.register(Booklet)
class BookletAdmin(TranslatableAdmin):
    list_display = ('title', 'all_languages_column', )

    fieldsets = (
        (None,
         {'fields': ('title', 'slug', 'teaser', 'booklet', 'cover', ), }),
        ('Publishing',
         {'fields': (('release_date', ), ('published', 'featured', ),), }),
        (None,
         {'fields': ('story', ), }),
    )

    def get_prepopulated_fields(self, request, obj=None):
        return {
            'slug': ('title',),
        }


