from django.conf.urls import url
import views


urlpatterns = [

    url(r'^home/$', views.profile, name='home'),
    url(r'^pages/about/$', views.about, name='about'),

    ]
