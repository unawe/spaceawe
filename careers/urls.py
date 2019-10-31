from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.CareersViewList.as_view(), name='list'),
    url(r'^category/(?P<category>\w+)/$', views.CareersViewList.as_view(), name='list_by_category'),
    url(r'^career/(?P<slug>[\w-]+)?/$', views.CareerDetailsView.as_view(), name='career-detail'),
    url(r'^career/(?P<slug>[\w-]+)/print-preview/$', views.CareerDetailPrintView.as_view(), name='print-preview'),
    url(r'^career/(?P<slug>[\w-]+)/first-page-preview/$', views.CareerDetailFirstPagePrintView.as_view(), name='print-preview-header'),
    url(r'^career/(?P<slug>[\w-]+)/content-preview/$', views.CareerDetailContentPrintView.as_view(), name='print-preview-content'),
    url(r'^interview/(?P<slug>.+)?/$', views.InterviewDetailsView.as_view(), name='interview-detail'),
    url(r'^webinar/(?P<slug>.+)?/$', views.WebinarDetailsView.as_view(), name='webinar-detail'),
    url(r'^teaching-material/(?P<slug>.+)?/$', views.TeachingMaterialDetailsView.as_view(), name='teaching-material-detail'),
    url(r'^booklet-download/(?P<slug>.+)?/$', views.BookletDetailView.as_view(), name='booklet-download'),
]
