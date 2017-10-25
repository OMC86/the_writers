# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from post.models import Post, Competition
from accounts.models import User
from django.utils import timezone


# Create your views here.
def about(request):
    return render(request, 'about.html')


# renders the home page
def profile(request):
    """
    Here we get the number of subscribers to calculate the competition prize.
    Then retrieve the two most recent featured posts to be rendered.
    Check if there are any finished competitions which didn't receive any entries or votes
    and delete them if that is the case, handled by the invalid_comp_check.
    Check if there is an active competition at this time. If there is, check the
    users subscription status, check what stage of the competition we are in and
    render these checks to the home page template.
    """
    subscribers = User.objects.filter(subscription_end__gte=timezone.now())
    prize = subscribers.count()
    # Get two featured posts
    posts = Post.objects.filter(is_featured=True).order_by('-date_published')[:2]
    # Check if the competition has entries and votes by the end of respective periods and if not delete the comp.
    competition = Competition.objects.all()
    for comp in competition:
        comp.invalid_comp_check()
    # Check if the comp is active
        if comp.is_active() and request.user.is_authenticated():
            subscribed = request.user.check_subscription()
            entry_period = comp.can_enter()
            vote_period = comp.can_vote()

            return render(request, 'home.html', {
                'posts': posts, 'comp': comp, 'prize': prize, 'subscribed': subscribed, 'entry_period': entry_period,
                'vote_period': vote_period})
    else:
        return render(request, 'home.html', {'posts': posts, 'prize': prize, 'users': subscribers})
