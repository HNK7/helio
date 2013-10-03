from django.conf.urls import patterns, include, url
from tourney import views


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'helio.views.home', name='home'),
    # url(r'^helio/', include('helio.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^100k/', views.qualify_point, name='qualify_point'),
    url(r'^22k/', include('tourney.urls', namespace='22k')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'tourney/login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/22k/'}, name='logout'),
)
