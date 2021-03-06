from django.conf.urls import url
from django.contrib.auth import views as auth_views
import views


urlpatterns = [
    url(r'^$', views.landing, name='landing'),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^accounts/logout/$', views.logout, name='logout'),
    url(r'^accounts/subscribe/$', views.subscribe, name='subscribe'),
    url(r'^accounts/cancel/$', views.cancel_subscription, name='cancel'),
    url(r'^accounts/upload/$', views.upload, name='upload'),

    # Password reset
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),


    # Webhooks
    url(r'^subscriptions_webhook/$', views.subscriptions_webhook, name='subscriptions_webhook'),
]
