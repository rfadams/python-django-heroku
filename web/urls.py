from django.conf.urls.defaults import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.contrib import admin

from web.accounts.views import CreateUserView, EditUserView


admin.autodiscover()
urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='home/homepage.html'), name='homepage'),

    #Example URLConf: url(r'^barns', include('barns.urls', namespace='barns', app_name='barns')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/login'}, name='logout'),

    url(r'^signup$', CreateUserView.as_view(), name='signup'),
    url(r'^profile$', TemplateView.as_view(template_name='accounts/profile.html'), name='profile'),
    url(r'^profile/edit$', EditUserView.as_view(), name='profile-edit'),
    url(r'^profile/edit/password$', 'django.contrib.auth.views.password_change', {'template_name': 'generic/form.html', 'post_change_redirect': '/profile'}, name='profile-editpassword'),
)