from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = patterns('',
    url(r'^$', 'salinity_front.views.index'),
    url(r'^job/$', 'salinity_front.views.job'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico'))
)
