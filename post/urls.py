from django.conf.urls import url
import views

urlpatterns = [
    url(r'posts/$', views.post_list),
    url(r'^posts/(?P<id>\d+)/$', views.post_detail),
]