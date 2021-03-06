# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from post.models import Post
from django.shortcuts import render, get_object_or_404, redirect
from filters import PostFilter
from comments.forms import CommentForm
from post.models import Competition
from django.contrib.auth.decorators import login_required


# There is a link in the readme to the tutorial I used to implement django.filter logic
def search(request):
    post_list = Post.objects.all()
    post_filter = PostFilter(request.GET, queryset=post_list)
    return render(request, 'search.html', {'posts': post_filter})


@login_required
def search_detail(request, id):
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
        comps = Competition.objects.all()
        for comp in comps:
            if comp.can_vote():
                args = {'post': post, 'form': form, 'comp': comp}
                return render(request, 'search_detail.html', args)
        else:
            args = {'post': post, 'form': form}
            return render(request, 'search_detail.html', args)
