from django.conf.urls import patterns, url

from ui import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^idle', views.idle, name='idle'),
    url(r'^weather$', views.weather, name='weather'),
    url(r'^statistics$', views.statistics, name='statistics'),
    url(r'^pdf/$', views.pdf, name='pdf')
)