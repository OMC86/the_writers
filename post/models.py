# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from writers import settings
from datetime import datetime
# Create your models here.


class Post(models.Model):

    POEM = 'PO'
    SHORT = 'SH'
    ESSAY = 'ES'
    MEMOIR = 'ME'
    LETTER = 'LE'
    SCRIPT = 'SC'
    SPEECH = 'SP'
    EXPOSE = 'EX'
    ARGUMENT = 'AR'
    OPINION = 'OP'
    COMEDY = 'CO'
    DRAMA = 'DR'
    HORROR = 'HO'
    ROMANCE = 'RO'
    TRAGEDY = 'TR'
    TRAGICOM = 'TC'
    FANTASY = 'FA'
    MYTH = 'MY'

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

    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    category = models.CharField(max_length=2, choices=TYPE, default="")
    genre = models.CharField(max_length=2, choices=GENRE, default="")
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=3000)
    date_created = models.DateTimeField(auto_now_add=True)
    date_published = models.DateTimeField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_entry = models.BooleanField(default=False)
    vote_count = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    image = models.ImageField(upload_to="images", blank=True, null=True)
    comp = models.ForeignKey('Competition', blank=True, null=True)

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
    is_active = models.BooleanField(default=False)
    can_vote = models.BooleanField(default=False)

    def _is_active(self):
        now = timezone.now()
        if self.entry_period_start < now < self.entry_period_fin:
            self.is_active = True
            self.save()

    def _can_vote(self):
        now = timezone.now()
        if self.vote_period_start < now < self.vote_period_end:
            self.can_vote = True
            self.save()

    def __unicode__(self):
        return self.title

