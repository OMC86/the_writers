from django.conf.urls import url
import views

urlpatterns = [
    # posts
    url(r'posts/$', views.post_list, name='post_list'),
    url(r'^posts/(?P<id>\d+)/$', views.post_detail),
    url(r'^posts/new/$', views.new_post, name='new_post'),
    url(r'^posts/(?P<id>\d+)/edit$', views.edit_post, name='edit'),
    url(r'^posts/(?P<id>\d+)/delete$', views.delete_post, name='delete'),

    # competition
    url(r'^competition/$', views.show_competition, name='view_comp'),
    url(r'^competition/entries/$', views.comp_entries, name='view_entries'),
    url(r'^competition/entries/(?P<id>\d+)/$', views.entry_detail, name='entry_detail'),
    
    

    # featured
    url(r'^featured/$', views.featured, name='featured'),
    url(r'^featured/(?P<id>\d+)/$', views.featured_detail, name='featured_detail'),
]