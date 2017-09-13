# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db import models
from django.utils import timezone
from writers import settings
from post.models import Post
# Create your models here.


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post, related_name='comments')
    content = models.TextField(max_length=3000)
    date_created = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.content
