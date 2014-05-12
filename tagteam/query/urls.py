from django.conf.urls import patterns, url

from query import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^processquery/$', views.processquery, name='processquery'),
    url(r'^getpost/(?P<post_id>\d+)/?$', views.getpost, name='getpost'),
)

