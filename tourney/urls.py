from django.conf.urls import patterns, url
from tourney import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<t_id>\d+)/$', views.detail, name='detail'),
    url(r'^entry/(?P<t_id>\d+)/$', views.entry, name='entry'),
    url(r'^player/$', views.player, name='directory'),
    url(r'^player/(?P<p_id>\d+)/$', views.profile, name='profile'),
    url(r'^player/edit/(?P<p_id>\d+)/$', views.profile_edit, name='profile_edit'),
    url(r'^card/(?P<rfid_id>\d+)/$', views.card, name='card'),
    url(r'^reg/$', views.register, name='register'),
)
