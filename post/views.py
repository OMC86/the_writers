# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages, auth
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from .models import Post, Competition
from .forms import PostForm
import stripe
import arrow


# renders a list of posts descending order
def post_list(request):
    posts = Post.objects.filter(date_published__lte=timezone.now()
                                ).order_by('-date_published')
    return render(request, 'posts/postlist.html', {'posts': posts})


def post_detail(request, id):
    post = get_object_or_404(Post, pk=id)
    post.views += 1
    post.save()
    return render(request, "posts/postdetail.html", {'post': post})


def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.date_published = timezone.now()

            if post.is_entry:
                user = request.user
                end = user.subscription_end
                now = arrow.now()
                if now < end:
                    competition = Competition.objects.all()
                    for comp in competition:
                        comp._is_active()

                    a = Competition.objects.get(is_active=True)
                    post.comp = a
                    post.save()

                    return redirect(post_detail, post.pk)
                else:
                    messages.error(request, "Please subscribe to enter competition")
                    return redirect(new_post)
            else:
                post.save()
                return redirect(post_detail, post.pk)
    else:
        form = PostForm()
    return render(request, 'posts/postform.html', {'form': form})


def edit_post(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.date_published = timezone.now()
            post.save()
            return redirect(post_detail, post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/postform.html', {'form': form})


def show_competition(request):
    competition = Competition.objects.all()
    for x in competition:
        x._is_active()

    comp = Competition.objects.filter(is_active=True)
    return render(request, 'competition/comp.html', {'comp': comp})







