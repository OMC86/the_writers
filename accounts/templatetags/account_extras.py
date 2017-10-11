from django import template
from django.utils import timezone
from accounts.models import User


register = template.Library()


@register.simple_tag
def count_users():
    return User.objects.all().count()