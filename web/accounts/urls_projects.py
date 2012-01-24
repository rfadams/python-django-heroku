from django.conf.urls.defaults import patterns, include, url
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from accounts.views import CreateProjectView

from django.contrib.auth.models import User

urlpatterns = patterns('',
    url(r'^new$', CreateProjectView.as_view(), name='new'),
)
