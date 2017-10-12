# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Comment
from django.contrib import messages
from post.views import featured_detail
from forms import CommentForm
# Create your views here.


@login_required
def delete_comment(request, id, com):
    comment = get_object_or_404(Comment, pk=com)
    comment.delete()
    messages.success(request, "Your comment was deleted")
    return redirect(featured_detail, id)


@login_required
def edit_comment(request, id, com):
    comment = get_object_or_404(Comment, pk=com)
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            comment.content = form.save()
            return redirect(featured_detail, id)
    else:
        form = CommentForm(instance=comment)
        return render(request, 'comments/editcomment.html', {'form': form})

