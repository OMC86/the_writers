# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.conf import settings
from post.models import Post


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post, related_name='comment')
    content = models.TextField(max_length=1000)
    date_created = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.content
