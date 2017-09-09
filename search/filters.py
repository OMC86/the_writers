from post.models import Post
import django_filters


class PostFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(name='title', lookup_expr='icontains')
    class Meta:
        model = Post
        fields = ['author', 'category', 'genre', 'is_entry', 'comp']
