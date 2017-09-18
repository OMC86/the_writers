from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.landing),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^accounts/logout/$', views.logout, name='logout'),
    url(r'^accounts/subscribe/$', views.subscribe, name='subscribe'),
    url(r'^accounts/cancel/$', views.cancel_subscription, name='cancel'),
    url(r'^accounts/upload/$', views.upload, name='upload'),


    # Webhooks
    url(r'^subscriptions_webhook/$', views.subscriptions_webhook, name='subscriptions_webhook'),
]