from django.conf.urls.defaults import patterns, include, url
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from django.contrib.auth.models import User

from accounts.models import *
from accounts.views import *

urlpatterns = patterns('',
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/login'}, name='logout'),

    url(r'^signup$', CreateUserView.as_view(), name='signup'),
    url(r'^account$', TemplateView.as_view(template_name='accounts/profile.html'), name='profile'),
    url(r'^account/edit$', EditUserView.as_view(), name='edit'),
    url(r'^account/edit/password$', 'django.contrib.auth.views.password_change', {'template_name': 'generic/form.html', 'post_change_redirect': '/account'}, name='password_change'),
)

#Groups
urlpatterns += patterns('', 
    url(r'^account/group$', GroupDetailView.as_view(), name='group'),
    url(r'^account/group/withdraw$', GroupWithdrawView.as_view(), name='group-withdraw'),
    url(r'^account/group/invite$', GroupSendInviteView.as_view(), name='group-invite'),
    # url(r'^(?P<slug>[-\w]+)/group/join$', GroupJoinView.as_view(), name='group-join'),
    # url(r'^account/group/requests$', GroupJoinRequestsView.as_view(), name='group-requests'),
)

#Invites
urlpatterns += patterns('', 
    url(r'^invites/(?P<slug>[-\w]+)$', group_accept_invite_view, name='invite'),
    url(r'^invites/(?P<slug>[-\w]+)/newuser$', GroupViewInviteNewUser.as_view(), name='invite-newuser'),
)

#User
urlpatterns += patterns('', 
    url(r'^(?P<slug>[-\w]+)$', DetailView.as_view(model=User, slug_field='username', template_name='generic/detail.html'), name='user'),
    url(r'^(?P<slug>[-\w]+)/group$', GroupDetailView.as_view(), name='user-group'),
)

#Projects
urlpatterns += patterns('', 
    url(r'^(?P<username>\w+)/(?P<slug>[-\w]+)$', DetailView.as_view(model=Project, template_name='generic/detail.html'), name='project'),
    url(r'^(?P<username>\w+)/(?P<slug>[-\w]+)/edit$', UpdateProjectView.as_view(), name='project-edit'),
)
