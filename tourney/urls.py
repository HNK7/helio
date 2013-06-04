from django.conf.urls import patterns, url
from tourney import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^tourney/(?P<t_id>\d+)/$', views.tourney_dashboard, name='tourney_dashboard'),
    url(r'^tourney/create/$', views.tourney_create, name='tourney_create'),
    url(r'^event/create/(?P<t_id>\d+)/$', views.event_create, name='event_create'),
    url(r'^event/edit/(?P<e_id>\d+)/$', views.event_edit, name='event_edit'),
    url(r'^(?P<t_id>\d+)/$', views.detail, name='detail'),
    url(r'^entry/(?P<t_id>\d+)/$', views.entry, name='entry'),
    url(r'^player/$', views.player, name='directory'),
    url(r'^player/(?P<p_id>\d+)/$', views.profile, name='profile'),
    url(r'^player/edit/(?P<p_id>\d+)/$', views.profile_edit, name='profile_edit'),
    url(r'^signup/(?P<e_id>\d+)/$', views.event_signup, name='event_signup'),
    url(r'^card/(?P<rfid_id>\d+)/$', views.card, name='card'),
    url(r'^reg/$', views.register, name='register'),
)
