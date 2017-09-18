# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from post.models import Post
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from filters import PostFilter
from comments.forms import CommentForm
from post.models import Competition
# Create your views here.


def search(request):
    post_list = Post.objects.all()
    post_filter = PostFilter(request.GET, queryset=post_list)
    return render(request, 'search.html', {'posts': post_filter})


def search_detail(request, id):
    x = timezone.now()
    post = get_object_or_404(Post, pk=id)
    post.views += 1
    post.save()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect(search_detail, post.id)
    else:
        form = CommentForm()
        comp = Competition.objects.all()
        for c in comp:
            if c.can_vote():
                return render(request, 'search_detail.html', {'post': post, 'form': form, 'c': c})
        else:
            return render(request, 'search_detail.html', {'post': post, 'form': form, 'x': x})

