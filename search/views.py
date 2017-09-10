# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from post.models import Post
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from filters import PostFilter
# Create your views here.


def search(request):
    post_list = Post.objects.all()
    post_filter = PostFilter(request.GET, queryset=post_list)
    return render(request, 'search.html', {'posts': post_filter})



def search_detail(request, id):
    post = get_object_or_404(Post, pk=id)
    post.views += 1
    post.save()
    return render(request, 'search_detail.html', {'post': post})

