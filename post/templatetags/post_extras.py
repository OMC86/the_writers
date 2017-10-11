from django import template
from django.utils import timezone
from post.models import Post, Competition
from accounts.models import User
import random
import arrow

register = template.Library()

# https://stackoverflow.com/questions/28837511/django-template-how-to-randomize-order-when-populating-page-with-objects

# Shuffle competition entries
@register.filter
def shuffle(arg):
    tmp = list(arg)[:]
    random.shuffle(tmp)
    return tmp


# Get the number of posts on the writers
@register.simple_tag
def get_total_posts():
    return Post.objects.all().count()


# Get the number of competitions
@register.simple_tag
def get_total_comps():
    return Competition.objects.all().count()


# Get the total sum of prize money
@register.simple_tag
def total_prize():
    comps = Competition.objects.filter(winner=True)
    prize_list = []
    for c in comps:
        prize_list.append(c.prize)
    return sum(prize_list)


# Check if comp can vote for base template show hide vote button
@register.simple_tag
def can_vote_comp():
    comps = Competition.objects.all().order_by('-vote_period_end')
    comp = comps[0]
    return comp.can_vote()
