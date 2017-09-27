# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from post.models import Post, Competition
from accounts.models import User
from django.utils import timezone

# Create your views here.
# This view renders the base template after login which is the profile home page


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def faq(request):
    return render(request, 'faq.html')


def profile(request):
    x = timezone.now()
    subscribers = User.objects.filter(subscription_end__gte=timezone.now())
    prize = subscribers.count()
    posts = Post.objects.filter(is_featured=True).order_by('-date_published')[:2]
    competition = Competition.objects.all()
    for comp in competition:
        if comp.is_active():
            return render(request, 'home.html', {'posts': posts, 'comp': comp, 'prize': prize, 'users': subscribers,
                                                 'x': x})
    else:
        return render(request, 'home.html', {'posts': posts, 'prize': prize, 'users': subscribers, 'x': x})


