# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.utils import timezone
from .models import Post, Competition, Vote
from .forms import PostForm


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
                now = timezone.now()
                if now < end:
                    competition = Competition.objects.all()
                    for comp in competition:
                        if comp.can_enter():
                            post.comp = comp
                            post.save()
                            return redirect(post_detail, post.pk)
                    else:
                        messages.error(request, "The entry period has either finished or not begun")
                        return redirect(new_post)
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

            if post.is_entry:
                user = request.user
                end = user.subscription_end
                now = timezone.now()
                if now < end:
                    competition = Competition.objects.all()
                    for comp in competition:
                        if comp.can_enter():
                            post.comp = comp
                            post.save()
                            return redirect(post_detail, post.pk)
                    else:
                        messages.error(request, "The entry period has either finished or not begun")
                        return redirect(new_post)

                else:
                    messages.error(request, "Please subscribe to enter competition")
                    return redirect(new_post)
            else:
                post.save()
                return redirect(post_detail, post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/postform.html', {'form': form})


def delete_post(request, id):
    post = get_object_or_404(Post, pk=id)
    post.delete()

    messages.success(request, "Your post was deleted")
    return redirect(post_list)


def show_competition(request):
    competition = Competition.objects.all()
    for comp in competition:
        if comp.is_active():
            return render(request, 'competition/comp.html', {'comp': comp})
    else:
        return render(request, 'competition/comp.html', {'comp': comp})


def comp_entries(request):
    entries = Post.objects.filter(is_entry=True)
    competition = Competition.objects.all()
    for comp in competition:
        if comp.is_active():
            return render(request, 'competition/entrylist.html', {'entries': entries, 'comp': comp})
    else:
        return render(request, 'competition/entrylist.html', {'entries': entries, 'comp': comp})


def entry_detail(request, id):
    post = get_object_or_404(Post, pk=id)
    post.views += 1
    post.save()
    voteobjects = Vote.objects.filter(post_id=post).values('voter')
    votes = voteobjects.all().count()
    return render(request, "competition/entrydetail.html", {'post': post, 'votes': votes, 'voteobjects': voteobjects})


@login_required
def cast_vote(request, id):
    post = get_object_or_404(Post, pk=id)
    competition = Competition.objects.all()
    for comp in competition:
        if comp.can_vote():
            new_vote, created = Vote.objects.get_or_create(voter=request.user,
                                                           post_id=post, comp=comp)
            if not created:
                messages.info(request, "You have already voted for this entry")
                return redirect(entry_detail, post.pk)
            else:
                messages.info(request, "Thanks for voting")
                return redirect(entry_detail, post.pk)
    else:
        messages.info(request, "Voting closed")
        return redirect(entry_detail, post.pk)


def featured(request):
    posts = Post.objects.filter(is_featured=True, date_published__lte=timezone.now()
                                ).order_by('-date_published')
    return render(request, 'featured/featuredlist.html', {'posts': posts})


def featured_detail(request, id):
    post = get_object_or_404(Post, pk=id)
    post.views += 1
    post.save()
    return render(request, "featured/featureddetail.html", {'post': post})
