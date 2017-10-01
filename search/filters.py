from post.models import Post
import django_filters as filters


class PostFilter(filters.FilterSet):
    author__username = filters.CharFilter(label="Author's username")
    title = filters.CharFilter(name='title', lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ['author__username', 'title', 'category', 'genre', 'comp']
