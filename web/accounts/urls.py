from django.conf.urls.defaults import patterns, include, url
from django.views.generic.base import TemplateView

from web.accounts.views import CreateUserView, EditUserView

urlpatterns = patterns('',
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/login'}, name='logout'),

    url(r'^signup$', CreateUserView.as_view(), name='signup'),
    url(r'^profile$', TemplateView.as_view(template_name='accounts/profile.html'), name='profile'),
    url(r'^profile/edit$', EditUserView.as_view(), name='edit'),
    url(r'^profile/edit/password$', 'django.contrib.auth.views.password_change', {'template_name': 'generic/form.html', 'post_change_redirect': '/profile'}, name='password_change'),
)