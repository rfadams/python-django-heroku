from django.conf.urls.defaults import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib import admin
from django.conf import settings

admin.autodiscover()
urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='home/homepage.html'), name='homepage'),
    url(r'', include('accounts.urls', namespace='accounts', app_name='accounts')),    

    #Example URLConf: url(r'^barns', include('barns.urls', namespace='barns', app_name='barns')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.PRODUCTION: 
    urlpatterns += patterns('',
        url(r'^public/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
