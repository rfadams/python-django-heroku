from django.conf.urls.defaults import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib import admin

admin.autodiscover()
urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='home/homepage.html'), name='homepage'),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^projects/', include('accounts.urls_projects', namespace='projects', app_name='accounts')),
    url(r'', include('accounts.urls', namespace='accounts', app_name='accounts')),
)
