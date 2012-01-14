from django.conf.urls.defaults import patterns, include, url
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView

from web.barns.models import Barn

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(model=Barn, template_name='generic/list.html'), name='list'),
    url(r'^/(?P<pk>\d+)$', DetailView.as_view(model=Barn, template_name='generic/detail.html'), name='detail'),
    
    url(r'^/new$', CreateView.as_view(model=Barn, template_name='generic/form.html', success_url='/barns/%(id)s'), name='create'),
    url(r'^/(?P<pk>\d+)/edit$', UpdateView.as_view(model=Barn, template_name='generic/form.html', success_url='/barns/%(id)s'), name='edit'),
)
