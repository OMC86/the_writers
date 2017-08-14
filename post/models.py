# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from writers import settings

# Create your models here.


class Post(models.Model):

    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    category = models.CharField(max_length=50)
    sub_category = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=3000)
    date_created = models.DateTimeField(auto_now_add=True)
    date_published = models.DateTimeField(blank=True, null=True)
    is_featured = False
    is_entry = False
    vote_count = 0

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __unicode__(self):
        return self.title
