from django.conf.urls import url
from django_filters.views import FilterView
from filters import PostFilter
import views

urlpatterns = [

    # filter
    url(r'^search/$', FilterView.as_view(filterset_class=PostFilter,
                                         template_name='search.html'), name='search'),

    # list all posts related to a single user
    url(r'^search/(?P<id>\d+)/$', views.search_user, name='search_user'),
    url(r'^search/(?P<id>\d+)/(?P<post_id>\d+)/$', views.user_post, name='user_post'),

]