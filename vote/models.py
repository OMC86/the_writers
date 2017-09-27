# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from post.models import Competition, Post
from writers import settings


# Create your models here.
class Vote(models.Model):
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='votes')
    comp = models.ForeignKey(Competition, related_name='votes')
    post_id = models.ForeignKey(Post, related_name='votes')
