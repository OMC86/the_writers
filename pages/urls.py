from django.conf.urls import url
import views


urlpatterns = [

    url(r'^home/$', views.profile, name='home'),
    url(r'^pages/about/$', views.about, name='about'),
    url(r'^pages/contact/$', views.contact, name='contact'),
    url(r'^pages/faq/$', views.faq, name='faq'),

    ]
