# from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.db.models import Q, F, Case, When

from django.views.generic import TemplateView
from django.http import Http404

from parler.views import ViewUrlMixin
from parler.utils.context import switch_language
from el_pagination.decorators import page_template

from django_ext.models.spaceawe import CATEGORIES
from spacescoops.models import Article
from activities.models import Activity
from games.models import Game

from news.models import Highlight
from institutions.models import Person


def home(request):
    # highlight are only. for better ordering, prepopulation is needed
    objects = Highlight.objects.all().select_related().annotate(
        release_date=Case(
            When(~Q(news_id=None), then=F('news__release_date')),
            When(~Q(scoop_id=None), then=F('scoop__release_date')),
            When(~Q(game_id=None), then=F('game__release_date')),
            When(~Q(activity_id=None), then=F('activity__release_date')),
            When(~Q(interview_id=None), then=F('interview__release_date')),
            When(~Q(career_id=None), then=F('career__release_date')),
        )
    ).order_by('release_date')

    return render(request, 'spaceawe/home.html', {
        'highlights': objects,
    })


def about(request):
    q = Q(spaceawe_partner=True) | Q(spaceawe_node=True)
    q = q & Q(institution__location__latitude__isnull=False)
    q = q & Q(institution__location__longitude__isnull=False)
    return render(request, 'spaceawe/about.html', {
        'partners': Person.objects.filter(q).select_related('institution').order_by('spaceawe_partner'),
    })


@page_template('spacescoops/article_list_page_in_category.html', key='scoops_page')
@page_template('games/game_list_page_in_category.html', key='games_page')
@page_template('activities/activity_list_page_in_category.html', key='activities_page')
def categories(request, code, template='spaceawe/categories.html', extra_context=None):
    if code not in CATEGORIES.keys():
        raise Http404
    context = {
        # we will get four of them even though we'll only display three
        # so that we can tell if we need to show the load more button
        'scoops': Article.add_prefetch_related(Article.objects.filter(**{code: True}).active_translations())[:3],
        'scoops_len': len(Article.add_prefetch_related(Article.objects.filter(**{code: True}).active_translations())),
        'games': Game.objects.available().filter(**{code: True})[:3],
        'games_len': len(Game.objects.available().filter(**{code: True})),
        'activities': Activity.objects.available().filter(**{code: True})[:3],
        'activities_len': len(Activity.objects.available().filter(**{code: True})),
        'spaceawe_category': code,
        'category': code,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


class TranslatableTemplateView(ViewUrlMixin, TemplateView):
    pass
