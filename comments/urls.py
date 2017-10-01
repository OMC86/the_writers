from django.conf.urls import url
import views

urlpatterns = [

    url(r'^featured/(?P<id>\d+)/(?P<com>\d+)$', views.delete_comment, name='delete_comment'),
    url(r'^featured/edit/(?P<id>\d+)/(?P<com>\d+)$', views.edit_comment, name='edit_comment'),

    ]
