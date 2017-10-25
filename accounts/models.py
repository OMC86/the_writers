# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField


"""
 I used the lessons on code institute to write the user model
 however I decided to keep the username field as to be
 displayed on the users profile page and used to identify the
 author of posts and comments. The email is used only to log
 users in and reset passwords.
 """


class AccountUserManager(UserManager):
    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):

        now = timezone.now()
        if not email:
            raise ValueError('The username must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractUser):

    stripe_id = models.CharField(max_length=40, default='', blank=True, null=True)
    subscription_end = models.DateTimeField(default=timezone.now)
    avatar = CloudinaryField("avatar", blank=True, null=True)
    objects = AccountUserManager()

    def check_subscription(self):
        now = timezone.now()
        return self.subscription_end > now
