from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'home/homepage.html'}),
    (r'^login$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}),
    (r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/login'}),

    (r'^accounts/profile/$', 'django.views.generic.simple.direct_to_template', {'template': 'accounts/profile.html'}),

    # Examples:
    # url(r'^$', 'lib.views.home', name='home'),
    # url(r'^lib/', include('lib.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
