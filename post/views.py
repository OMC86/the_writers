# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.utils import timezone
from .models import Post, Competition
from vote.models import Vote
from accounts.models import User
from accounts.views import subscribe
from .forms import PostForm
from comments.forms import CommentForm


# renders a users posts in descending order
@login_required
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


# Renders a specific post and comment form
def post_detail(request, id):
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
    args = {'post': post, 'form': form}
    return render(request, "posts/postdetail.html", args)


@login_required 
def new_post(request):
    context = dict(backend_form=PostForm())
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
                # Check if user is subscribed
                if post.author.check_subscription():
                    competition = Competition.objects.all()
                    # Check if the competition is active and save post as entry
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
                    # if the entry period has finished
                    else:
                        messages.error(request, "The entry period has ended for the current competition")
                        return redirect(new_post)
                # if user is not subscribed send them to subscription form
                else:
                    messages.error(request, "Please subscribe to enter competition")
                    return redirect(subscribe)
            # if featured post save published date
            elif post.is_featured:
                post.date_published = timezone.now()
                post.save()
                return redirect(post_detail, post.pk)
            # if not featured and not a competition entry entry
            else:
                post.save()
                return redirect(post_detail, post.pk)

    return render(request, 'posts/postform.html', context)


@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, pk=id)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            post = form.save(commit=False)

            # if competition entry and user is subscribed
            if post.is_entry:
                post.date_published = timezone.now()
                user = request.user
                if user.check_subscription:
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
                    return redirect(new_post) # send to upgrade account
            # save date published if post is featured
            elif post.is_featured:
                post.date_published = timezone.now()
                post.save()
                return redirect(post_detail, post.pk)
            # if post is not featured or not entry
            else:
                post.save()
                return redirect(post_detail, post.pk)
        else:

            context = dict(backend_form=form.instance)
    else:
        context = dict(backend_form=PostForm(instance=post))
    return render(request, 'posts/postform.html', context)


@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, pk=id)
    post.delete()
    messages.success(request, "Your post was deleted")
    return redirect(post_list)


def show_competition(request):
    # Calculate the prize as number of subscribers
    subscribers = User.objects.filter(subscription_end__gte=timezone.now())
    prize = subscribers.count()

    competition = Competition.objects.all()
    for comp in competition:

        # get the currently active competition
        if comp.is_active() and request.user.is_authenticated():
            subscribed = request.user.check_subscription()
            entry_period = comp.can_enter()
            vote_period = comp.can_vote()
            args = {'comp': comp, 'entry_period': entry_period, 'vote_period': vote_period, 'subscribed': subscribed,
                    'prize': prize}
            return render(request, 'competition/comp.html', args)
    else:
        return render(request, 'competition/comp.html')


# Show the list of competition entries in the currently active competition
def comp_entries(request):
    entries = Post.objects.filter(is_entry=True)

    competition = Competition.objects.all()
    for comp in competition:
        if comp.is_active():
            entry_period = comp.can_enter()
            # If there were no entries during the entry period delete the competition
            if not entry_period and not comp.check_posts():
                comp.delete()
                return render(request, 'competition/entrylist.html')
            else:
                vote_period = comp.can_vote()
                args = {'entries': entries, 'comp': comp, 'entry_period': entry_period, 'vote_period': vote_period}
                return render(request, 'competition/entrylist.html', args)
    else:
        return render(request, 'competition/entrylist.html')


# detailed view of competition entry
@login_required
def entry_detail(request, id):
    post = get_object_or_404(Post, pk=id)
    post.views += 1
    post.save()
    vote_objects = Vote.objects.filter(post_id=post)
    votes = vote_objects.all().count()
    # comment form
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
        # check if user has voted for this entry already
        for vote in vote_objects:
            if vote.voter == request.user:
                args = {'post': post, 'votes': votes, 'vote': vote, 'form': form}
                return render(request, "competition/entrydetail.html", args)
        else:
            form = CommentForm()
        args = {'post': post, 'votes': votes, 'form': form}
        return render(request, "competition/entrydetail.html", args)


# Vote for entry
@login_required
def cast_vote(request, id):
    post = get_object_or_404(Post, pk=id)
    competition = Competition.objects.all()
    for comp in competition:
        # if the voting period is open get the vote or create a new vote if one hasn't already been created
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
    # get the most recent competition
    comp = competitions[0]

    def comp_del():
        if not comp.check_posts():
            comp.delete()
    # check if anyone has voted. If no one voted delete the competition and save the posts as not entered in a comp
        elif not comp.check_votes():
            entries = comp.post.all()
            for entry in entries:
                entry.is_entry = 0
                entry.comp = None
                entry.save()
            comp.delete()
        else:
            get_winners()

    # find the winner or winners of the most recent competition
    def get_winners():
        # Get all vote objects associated with comp and count how often the same post occurs in the votes
        votes = Vote.objects.filter(comp=comp)
        entries = votes.values_list('post_id').annotate(
            vote_count=Count('post_id'))
        # Find max votes. Add all posts with max votes to tied list
        #  (index[0] = post_id, index[1] = votes)
        max_val = max(votes[1] for votes in entries)
        tied = []
        for entry in entries:
            if entry[1] == max_val:
                tied.append(entry[0])
        # save the winners, calculate the prize and render the winners page
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


# Renders the winning post
@login_required
def winner_detail(request, id):
    post = get_object_or_404(Post, pk=id)
    post.views += 1
    post.save()
    vote_objects = Vote.objects.filter(post_id=post)
    votes = vote_objects.all().count()
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
    args = {'post': post, 'votes': votes, 'form': form}
    return render(request, 'competition/winnerdetail.html', args)


# renders a list of featured posts
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



@login_required
def featured_detail(request, id):
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
    args = {'post': post, 'form': form}
    return render(request, "featured/featureddetail.html", args)
