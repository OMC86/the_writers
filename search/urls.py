from django.conf.urls import url

import views

urlpatterns = [

    # filter
    url(r'^search/$', views.search, name='search'),

    # list all posts related to a single user
    url(r'^search/(?P<id>\d+)/$', views.search_detail, name='search_detail'),


]