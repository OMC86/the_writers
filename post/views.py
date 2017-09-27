# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.utils import timezone
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from .models import Post, Competition
from vote.models import Vote
from accounts.models import User
from .forms import PostForm
from comments.forms import CommentForm


# renders a list of posts descending order
def post_list(request):
    postlist = Post.objects.filter(author=request.user).order_by('-date_created')
    page = request.GET.get('page')

    paginator = Paginator(postlist, 6)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'posts/postlist.html', {'posts': posts})


def post_detail(request, id):
    x = timezone.now()
    post = get_object_or_404(Post, pk=id)
    post.views += 1
    post.save()
    return render(request, "posts/postdetail.html", {'post': post, 'x': x})


@login_required 
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            """
            First Check if the post is a competition entry. If so, check that the user 
            has an active subscription and finally check for a competition which 
            has an active entry period. If these conditions return true the post is saved 
            as a competition entry.
            """
            if post.is_entry:
                post.date_published = timezone.now()
                user = request.user
                end = user.subscription_end
                now = timezone.now()
                if now < end:
                    competition = Competition.objects.all()
                    for comp in competition:
                        if comp.can_enter():
                            post.comp = comp
                            post.save()
                            messages.info(request, "Your post has been entered. Please note that in the unlikely "
                                                   "event of there being no votes by the time the vote period ends, "
                                                   "the competition will be removed from The Writers database and your"
                                                   " entry will be re-assigned as not entered in a competition. Good"
                                                   " luck!")
                            return redirect(post_detail, post.pk)
                    else:
                        messages.error(request, "The entry period has ended for the current competition")
                        return redirect(new_post)
                else:
                    messages.error(request, "Please subscribe to enter competition")
                    return redirect(new_post)
            elif post.is_featured:
                post.date_published = timezone.now()
                post.save()
                return redirect(post_detail, post.pk)

            else:
                post.save()
                return redirect(post_detail, post.pk)
    else:
        form = PostForm()
    return render(request, 'posts/postform.html', {'form': form})


@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            if post.is_entry:
                post.date_published = timezone.now()
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
            elif post.is_featured:
                post.date_published = timezone.now()
                post.save()
                return redirect(post_detail, post.pk)

            else:
                post.save()
                return redirect(post_detail, post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/postform.html', {'form': form})


@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, pk=id)
    post.delete()
    messages.success(request, "Your post was deleted")
    return redirect(post_list)


def show_competition(request):
    x = timezone.now()
    competition = Competition.objects.all()
    subscribers = User.objects.filter(subscription_end__gte=timezone.now())
    prize = subscribers.count()
    for comp in competition:
        """
        get the currently active competition
        """
        if comp.is_active():
            return render(request, 'competition/comp.html', {'comp': comp, 'x': x, 'prize': prize})
    else:
        return render(request, 'competition/comp.html')


def comp_entries(request):
    x = timezone.now()
    entries = Post.objects.filter(is_entry=True)
    competition = Competition.objects.all()
    for comp in competition:
        if comp.is_active():
            if x > comp.entry_period_fin and not comp.check_posts():
                comp.delete()
                return render(request, 'competition/entrylist.html')
            else:
                return render(request, 'competition/entrylist.html', {'entries': entries, 'comp': comp, 'x': x})
    else:
        return render(request, 'competition/entrylist.html')


def entry_detail(request, id):
    x = timezone.now()
    post = get_object_or_404(Post, pk=id)
    post.views += 1
    post.save()
    voteobjects = Vote.objects.filter(post_id=post)
    votes = voteobjects.all().count()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect(entry_detail, post.id)
    else:
        form = CommentForm()
        for vote in voteobjects:
            if vote.voter == request.user:
                return render(request, "competition/entrydetail.html",
                              {'post': post, 'votes': votes, 'vote': vote, 'form': form, 'x': x})
        else:
            form = CommentForm()
            return render(request, "competition/entrydetail.html",
                          {'post': post, 'votes': votes, 'form': form, 'x': x})


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
        messages.info(request, "Voting hasn't begun yet")
        return redirect(entry_detail, post.pk)


def winners(request):
    # get all competitions and order them by most recent
    competitions = Competition.objects.all().order_by('-vote_period_end')
    page = request.GET.get('page')

    paginator = Paginator(competitions, 2)
    try:
        comps = paginator.page(page)
    except PageNotAnInteger:
        comps = paginator.page(1)
    except EmptyPage:
        comps = paginator.page(paginator.num_pages)

    # Get all past winning entries
    posts = Post.objects.filter(is_winner=True)
    # get the most recent competition. If no one entered delete the competition
    comp = competitions[0]

    def comp_del():
        if not comp.check_posts():
            comp.delete()
    # check if anyone has voted. If no one voted delete the competition and save the posts as not entered in a comp
        elif not comp.check_votes():
            p = comp.post.all()
            for x in p:
                x.is_entry = 0
                x.comp = None
                x.save()
            comp.delete()
        else:
            get_winners()

    # find the winner or winners of the most recent competition
    def get_winners():
        # Get all vote objects associated with comp and count how often the same post occurs in the votes
        x = Vote.objects.filter(comp=comp)
        entries = x.values_list('post_id').annotate(
            vote_count=Count('post_id'))
        # Find max votes. Add all posts with max votes to tied list
        #  (index[0] = post_id, index[1] = votes)
        max_val = max(x[1] for x in entries)
        tied = []
        for v in entries:
            if v[1] == max_val:
                tied.append(v[0])
            # check if there's more than one winner. If so save the winners and divide the prize between them,
            # then render the winners page
        if len(tied) > 1:
            champs = Post.objects.filter(id__in=tied)
            for c in champs:
                c.is_winner = 1
                c.save()

            comp.winner = 1
            comp.prize = comp.get_prize()
            comp.save()

            # If there is only one winner, save it, save the prize and render the winners page
        else:
            getentry = tied[0]
            entry = Post.objects.get(id=getentry)
            entry.is_winner = 1
            entry.save()

            comp.winner = 1
            comp.prize = comp.get_prize()
            comp.save()

    # Check if the most recent competition is still active, if it is render the winners page
    if comp.is_active():
        return render(request, 'competition/winnerlist.html', {'comps': comps, 'posts': posts})
    # If most recent comp has finished, check if anyone has entered. If they have get the winners
    elif not comp.winner:
        comp_del()
        return render(request, 'competition/winnerlist.html', {'comps': comps, 'posts': posts})
    # or if there were no entries or no comps without winners render the winners page
    else:
        return render(request, 'competition/winnerlist.html', {'comps': comps, 'posts': posts})


def winner_detail(request, id):
    x = timezone.now()
    post = get_object_or_404(Post, pk=id)
    post.views += 1
    post.save()
    voteobjects = Vote.objects.filter(post_id=post)
    votes = voteobjects.all().count()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect(winner_detail, post.id)
    else:
        form = CommentForm()
        return render(request, 'competition/winnerdetail.html', {'post': post, 'votes': votes, 'form': form, 'x': x})


def featured(request):
    postlist = Post.objects.filter(is_featured=True, date_published__lte=timezone.now()
                                ).order_by('-date_published')
    page = request.GET.get('page')

    paginator = Paginator(postlist, 6)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'featured/featuredlist.html', {'posts': posts})


def featured_detail(request, id):
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
            return redirect(featured_detail, post.id)
    else:
        form = CommentForm()
        return render(request, "featured/featureddetail.html", {'post': post, 'form': form, 'x': x})
