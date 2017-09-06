# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Post, Competition, Vote


admin.site.register(Post)
admin.site.register(Competition)
admin.site.register(Vote)
