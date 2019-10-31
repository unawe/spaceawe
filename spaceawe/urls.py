"""spaceawe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from django.views.generic import TemplateView, RedirectView

from contests.views import LatestCompetitionView
from .views import TranslatableTemplateView
from develop.views import DevelopView
from search.views import simple_search

urlpatterns = [
#    url(r'^admin/', include(admin.site.urls)),
    # url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
]

#urlpatterns += i18n_patterns(
#    url(r'^admin/', include(admin.site.urls)),
#)

urlpatterns += i18n_patterns(
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'spaceawe.views.home', name='home'),
    url(r'^categories/(?P<code>.+)?/$', 'spaceawe.views.categories', name='categories'),
    # url(r'^search/', simple_search, name='search'),
    url(r'^news/', include('news.urls', namespace='news'), name='news'),
    url(r'^scoops/', include('spacescoops.urls', namespace='scoops'),name='scoops'),
    url(r'^activities/', include('activities.urls', namespace='activities')),
    url(r'^games/', include('games.urls', namespace='games'),name='games'),
    url(r'^about/$', 'spaceawe.views.about', name='about'),
    # url(r'^soon/$', TranslatableTemplateView.as_view(template_name='spaceawe/soon.html', view_url_name='soon'), name='soon'),
    # url(r'^skills/$', TranslatableTemplateView.as_view(template_name='spaceawe/soon_skills.html', view_url_name='soon_skills'), name='soon_skills'),
    url(r'^skills/', include('develop.urls', namespace='develop')),
    # url(r'^careers/$', TranslatableTemplateView.as_view(template_name='spaceawe/soon_careers.html', view_url_name='soon_careers'), name='soon_careers'),
    url(r'^careers/', include('careers.urls', namespace='careers')),
    url(r'^competition$', LatestCompetitionView.as_view(), name='latest-competition'),
    url(r'^competition/', include('contests.urls', namespace='contests')),
    url(r'^search/', include('search.urls', namespace='search')),
    url(r'^download/', include('downloads.urls', namespace='downloads')),

)

if settings.DEBUG:
    # serve MEDIA_ROOT (uploaded files) in development
    from django.conf.urls.static import static
    import debug_toolbar

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        # test 404 and 500 pages
        url(r'^500/$', TemplateView.as_view(template_name='500.html')),
        url(r'^404/$', TemplateView.as_view(template_name='404.html')),

        # redirects (use nginx rewrite for production)
        url(r'^favicon\.ico/?$', RedirectView.as_view(url='/static/favicons/favicon.ico', permanent=True)),

        # # serve MEDIA_ROOT (uploaded files) in development
        # url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

        # # debug_toolbar
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
