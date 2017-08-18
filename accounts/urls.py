from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.landing),
    url(r'^home/$', views.profile, name='home'),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^accounts/logout/$', views.logout, name='logout'),
    url(r'^accounts/subscribe/$', views.subscribe, name='subscribe'),
    ]