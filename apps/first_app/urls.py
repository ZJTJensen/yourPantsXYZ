from django.conf.urls import url, include
from . import views

urlpatterns=[
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^success$', views.success),
    url(r'^login$', views.login),
    url(r'^message$', views.message),
    url(r'^load$', views.load),
    url(r'^logout$', views.logout),
    url(r'^delete/(?P<id>\d+)$', views.removeMessage),
    url(r'^ban/(?P<id>\d+)$', views.banUser),
    url(r'^unban/(?P<id>\d+)$', views.unbanUser),
    url(r'^admin/(?P<id>\d+)$', views.adminUser),
    url(r'^noadmin/(?P<id>\d+)$', views.noAdminUser),
    url(r'^find$', views.find),
]
