from django.conf.urls import patterns, url
from tourney import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^t/(?P<t_id>\d+)/$', views.tourney_dashboard, name='tourney_dashboard'),
    url(r'^t/c/$', views.tourney_create, name='tourney_create'),
    url(r'^e/c/(?P<t_id>\d+)/$', views.event_create, name='event_create'),
    url(r'^e/e/(?P<e_id>\d+)/$', views.event_edit, name='event_edit'),
    url(r'^n/(?P<t_id>\d+)/$', views.entry, name='entry'),
    url(r'^d_n/(?P<t_id>\d+)/(?P<entry_id>\d+)/$', views.del_entry, name='del_entry'),
    url(r'^nb/(?P<t_id>\d+)/$', views.entry_big, name='entry_big'),
    url(r'^p_r/(?P<t_id>\d+)/$', views.pre_register_list, name='pre_register_list'),
    url(r'^p_r/r/(?P<t_id>\d+)/(?P<p_id>\d+)/$', views.pre_register, name='pre_register'),
    url(r'^p_r/c/(?P<t_id>\d+)/$', views.pre_register_create, name='pre_register_create'),
    url(r'^p/$', views.player, name='directory'),
    url(r'^p/(?P<p_id>\d+)/$', views.profile, name='profile'),
    url(r'^p/e/(?P<p_id>\d+)/$', views.profile_edit, name='profile_edit'),
    url(r'^s/(?P<e_id>\d+)/$', views.event_signup, name='event_signup'),
    url(r'^d_t/(?P<e_id>\d+)/(?P<team_id>\d+)/$', views.del_team, name='del_team'),
    url(r'^r/(?P<t_id>\d+)/$', views.card, name='card'),
    url(r'^r/(?P<t_id>\d+)/(?P<rfid_id>\d+)/$', views.register, name='register'),
    url(r'^m/(?P<t_id>\d+)/$', views.payment, name='payment'),
    url(r'^m/(?P<t_id>\d+)/(?P<rfid_id>\d+)/$', views.payment, name='payment'),
    url(r'^d/(?P<e_id>\d+)/$', views.draw, name='draw'),
    url(r'^d/s/(?P<e_id>\d+)/$', views.send_draw_sms, name='draw_sms'),
    url(r'^b/(?P<e_id>\d+)/$', views.refree, name='refree'),
    url(r'^l/$', views.league_stat, name='league_stat'),


)
