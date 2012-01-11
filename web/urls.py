from django.conf.urls.defaults import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib import admin

from web.accounts.views import CreateUserView

admin.autodiscover()
urlpatterns = patterns('',
    (r'^$', TemplateView.as_view(template_name='home/homepage.html')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/login'}, name='logout'),

    url(r'^profile$', TemplateView.as_view(template_name='accounts/profile.html'), name='profile'),
    url(r'^signup$', CreateUserView.as_view(), name='signup'),
)