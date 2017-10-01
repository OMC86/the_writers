from django import template
from django.utils import timezone
from post.models import Post, Competition
import random
import arrow

register = template.Library()

# https://stackoverflow.com/questions/28837511/django-template-how-to-randomize-order-when-populating-page-with-objects


@register.filter
def shuffle(arg):
    tmp = list(arg)[:]
    random.shuffle(tmp)
    return tmp


@register.simple_tag
def get_total_posts():
    return Post.objects.all().count()


@register.simple_tag
def get_total_comps():
    return Competition.objects.all().count()


@register.simple_tag
def total_prize():
    comps = Competition.objects.filter(winner=True)
    prize_list = []
    for c in comps:
        prize_list.append(c.prize)
    return sum(prize_list)


@register.simple_tag
def active_comp():
    comps = Competition.objects.all().order_by('-vote_period_end')
    comp = comps[0]
    return comp.is_active()
