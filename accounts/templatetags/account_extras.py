from django import template
from django.utils import timezone
from accounts.models import User


register = template.Library()

@register.filter
def check_subscription(user):
    subscribers = []
    user = User.objects.filter(subscription_end__gte=timezone.now())
    for u in user:
        subscribers.append(u)
    return subscribers


@register.simple_tag
def count_subscribers():
    return User.objects.filter(subscription_end__gte=timezone.now()).count()


@register.simple_tag
def count_users():
    return User.objects.all().count()