# coding: utf8
from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^$', views.json_view),
    url(r'^(?P<pk>[0-9]+)/$', views.json_view),
]
