# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from post.models import Post
from accounts.models import User
from django.shortcuts import render, get_object_or_404
# Create your views here.


def search_user(request, id):
    user = get_object_or_404(User, pk=id)
    posts = Post.objects.filter(author=user)
    return render(request, 'post_by_user.html', {'posts': posts, 'user': user})


def user_post(request, id, post_id):
    user = get_object_or_404(User, pk=id)
    post = get_object_or_404(Post, pk=post_id)
    post.views += 1
    post.save()
    return render(request, 'post_by_user_detail.html', {'post': post})