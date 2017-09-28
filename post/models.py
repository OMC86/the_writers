# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from writers import settings
from django.db.models import Count
from datetime import datetime
from accounts.models import User

# Create your models here.


class Post(models.Model):

    POEM = 'Poem'
    SHORT = 'Short'
    ESSAY = 'Essay'
    MEMOIR = 'Memoir'
    LETTER = 'Letter'
    SCRIPT = 'Script'
    SPEECH = 'Speech'
    EXPOSE = 'Expose'
    ARGUMENT = 'Argument'
    OPINION = 'Opinion'
    COMEDY = 'Comedy'
    DRAMA = 'Drama'
    HORROR = 'Horror'
    ROMANCE = 'Romance'
    TRAGEDY = 'Tragedy'
    TRAGICOM = 'Tragic Comedy'
    FANTASY = 'Fantasy'
    MYTH = 'Myth'

    TYPE = (
        (None, ""),
        (POEM, 'Poem'),
        (SHORT, 'Short Story'),
        (ESSAY, 'Essay'),
        (MEMOIR, 'Memoir'),
        (LETTER, 'Letter'),
        (SCRIPT, 'script'),
        (SPEECH, 'Speech'),
    )

    GENRE = (
        ('Nonfiction', (
            (None, ""),
            (EXPOSE, 'Expository'),
            (ARGUMENT, 'Argumentative'),
            (OPINION, 'Opinion'),
        )
    ),
        ('Fiction', (
            (None, ""),
            (COMEDY, 'Comedy'),
            (DRAMA, 'Drama'),
            (HORROR, 'Horror'),
            (ROMANCE, 'Romance'),
            (TRAGEDY, 'Tragedy'),
            (TRAGICOM, 'Tragicomedy'),
            (FANTASY, 'Fantasy'),
            (MYTH, 'Mythology'),
        ))
    )

    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user')
    category = models.CharField(max_length=20, choices=TYPE, blank=True, null=True)
    genre = models.CharField(max_length=20, choices=GENRE, blank=True, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=3000)
    date_created = models.DateTimeField(auto_now_add=True)
    date_published = models.DateTimeField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_entry = models.BooleanField(default=False)
    is_winner = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    image = models.ImageField(upload_to="images", blank=True, null=True)
    comp = models.ForeignKey('Competition', blank=True, null=True, related_name='post')

    def publish(self):
        self.date_published = timezone.now()
        self.save()

    def __unicode__(self):
        return self.title


class Competition(models.Model):
    title = models.CharField(max_length=50)
    brief = models.CharField(max_length=300)
    entry_period_start = models.DateTimeField(blank=True, null=True)
    entry_period_fin = models.DateTimeField(blank=True, null=True)
    vote_period_start = models.DateTimeField(blank=True, null=True)
    vote_period_end = models.DateTimeField(blank=True, null=True)
    winner = models.BooleanField(default=False)
    prize = models.IntegerField(blank=True, null=True)

    def is_active(self):
        now = timezone.now()
        return self.entry_period_start < now < self.vote_period_end

    def can_enter(self):
        now = timezone.now()
        return self.entry_period_start < now < self.entry_period_fin

    def can_vote(self):
        now = timezone.now()
        return self.vote_period_start < now < self.vote_period_end

    def get_winner(self):
        now = timezone.now()
        return self.vote_period_end < now

    def check_votes(self):
        return self.votes.count()

    def check_posts(self):
        return self.post.count()

    def get_prize(self):
        subscribers = User.objects.filter(subscription_end__gte=timezone.now())
        prize = subscribers.count()
        return prize





    def __unicode__(self):
        return self.title
