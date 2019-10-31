import os

from django.http import HttpResponse
from django.views.generic import DetailView, TemplateView
from django.core.urlresolvers import reverse
from parler.views import ViewUrlMixin, TranslatableSlugMixin
from django.utils.timezone import datetime
from django.shortcuts import redirect, get_object_or_404

from django.conf import settings
from django_ext import compiler
from django.utils.translation import get_language
from django.http import Http404
from spaceawe import misc
from .models import Interview, Career, Webinar, TeachingMaterial, TeachingMaterialAttachment, Booklet


class CareersViewList(ViewUrlMixin, TemplateView):
    template_name = 'careers.html'
    careers_portion_template_name = 'careers/career_list_page.html'
    interviews_portion_template_name = 'interviews/interview_list_page.html'
    webinars_portion_template_name = 'webinars/webinar_list_page.html'
    teaching_materials_portion_template_name = 'teaching_material/teaching_material_list_page.html'
    view_url_name = 'careers:list'

    def filter_category(self, queryset):
        if 'category' in self.kwargs:
            category = self.kwargs['category']
            queryset = queryset.filter(**{category: True})
        return queryset

    def get_careers_queryset(self):
        queryset = Career.objects.all()
        queryset = self.filter_category(queryset).exclude(published=False).exclude(release_date__gte=datetime.today())
        return queryset

    def get_interviews_queryset(self):
        queryset = Interview.objects.all()
        queryset = self.filter_category(queryset).exclude(cover__isnull=True).exclude(published=False).exclude(release_date__gte=datetime.today())
        return queryset

    def get_webinars_queryset(self):
        queryset = Webinar.objects.all()
        queryset = self.filter_category(queryset).exclude(published=False).exclude(release_date__gte=datetime.today())
        return queryset

    def get_teaching_materials_queryset(self):
        queryset = TeachingMaterial.objects.all()
        queryset = self.filter_category(queryset).exclude(published=False).exclude(release_date__gte=datetime.today())
        return queryset

    def get_booklets_queryset(self):
        return Booklet.objects.available().last()

    def get_view_url(self):
        if 'category' in self.kwargs:
            return reverse('careers:list_by_category', kwargs={'category': self.kwargs['category']})
        else:
            return super().get_view_url()

    def get_template_names(self):
        if self.request.is_ajax():
            if self.request.GET.get('querystring_key') == 'carrers_page':
                return [self.careers_portion_template_name]
            if self.request.GET.get('querystring_key') == 'interviews_page':
                return [self.interviews_portion_template_name]
            if self.request.GET.get('querystring_key') == 'webinars_page':
                return [self.webinars_portion_template_name]
            if self.request.GET.get('querystring_key') == 'teaching_material_page':
                return [self.teaching_materials_portion_template_name]
        else:
            return super().get_template_names()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_template'] = self.template_name
        context['interviews'] = self.get_interviews_queryset()
        context['careers'] = self.get_careers_queryset()
        context['webinars'] = self.get_webinars_queryset()
        context['teaching_materials'] = self.get_teaching_materials_queryset()
        context['booklet'] = self.get_booklets_queryset()
        if 'category' in self.kwargs:
            context['category'] = self.kwargs['category']
        else:
            context['category'] = ''
        return context


class CareerDetailsView(ViewUrlMixin, TranslatableSlugMixin, DetailView):
    view_url_name = 'careers:career-detail'
    template_name = 'careers/detail.html'

    def get_interviews_queryset(self, career_id):
        queryset = Interview.objects.filter(career=career_id).exclude(published=False).exclude(release_date__gte=datetime.today())
        return queryset

    def get_queryset(self):
        queryset = Career.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interviews'] = self.get_interviews_queryset(context['object'].id)
        return context

    def get(self, request, *args, **kwargs):
        fmt = request.GET.get('format')
        career_id = request.GET.get('id')

        if hasattr(settings, 'CAREER_DOWNLOADS') and fmt in settings.CAREER_DOWNLOADS['renderers'].keys():
            url = compiler.get_career_generated_url(settings.CAREER_DOWNLOADS, fmt, career_id, lang=get_language())
            if not url:
                raise Http404
            return redirect(url)
        else:
            return super().get(request, args, kwargs)


class CareerDetailPrintView(CareerDetailsView):
    template_name = 'careers/career_detail_print.html'


class CareerDetailFirstPagePrintView(CareerDetailsView):
    # TODO now are pages separated from first page. Hide small logo with @page:first is not working. Could be done in future.
    template_name = 'careers/career_detail_print_firstpage.html'


class CareerDetailContentPrintView(CareerDetailsView):
    template_name = 'careers/career_detail_print_content.html'


class InterviewDetailsView(ViewUrlMixin, TranslatableSlugMixin, DetailView):
    view_url_name = 'careers:interview-detail'
    template_name = 'interviews/detail.html'

    def get_queryset(self):
        queryset = Interview.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['random'] = misc.spaceawe_random_resources(self.object)
        print('Test')
        return context


class WebinarDetailsView(ViewUrlMixin, TranslatableSlugMixin, DetailView):
    view_url_name = 'careers:webinar-detail'
    template_name = 'webinars/detail.html'

    def get_queryset(self):
        queryset = Webinar.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TeachingMaterialDetailsView(ViewUrlMixin, TranslatableSlugMixin, DetailView):
    view_url_name = 'careers:teaching-material-detail'
    template_name = 'teaching_material/detail.html'

    def get_queryset(self):
        queryset = TeachingMaterial.objects.all()
        return queryset

    def get_attachment_queryset(self):
        queryset = TeachingMaterialAttachment.objects.filter(hostmodel=self.object.id, show=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = [v['title'] for v in self.object.spaceawe_categories]
        context['attachments'] = self.get_attachment_queryset()
        return context


class BookletDetailView(DetailView):
    def post(self, request, *args, **kwargs):
        language = request.POST.get('item_language')
        slug = kwargs.get('slug')
        obj = get_object_or_404(Booklet, translations__slug=slug)
        obj.set_current_language(language)

        with open(obj.booklet.path, 'rb') as booklet_file:
            response = HttpResponse(booklet_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment;filename=%s' % os.path.basename(obj.booklet.name)
            return response