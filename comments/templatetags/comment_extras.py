from django import template
from comments.models import Comment

register = template.Library()


@register.simple_tag
def count_comments():
    return Comment.objects.all().count()
