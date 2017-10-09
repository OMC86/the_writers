# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from smartfields import fields
from smartfields.dependencies import FileDependency
from smartfields.processors import ImageProcessor


# https://stackoverflow.com/questions/6195478/max-image-size-on-file-upload
def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 5.0
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("Maximum file size is %sMB" % str(megabyte_limit))


# Create your models here.
class AccountUserManager(UserManager):
    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):

        now = timezone.now()
        if not email:
            raise ValueError('The given username must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractUser):

    stripe_id = models.CharField(max_length=40, default='')
    subscription_end = models.DateTimeField(default=timezone.now)
    avatar = fields.ImageField(dependencies=[
        FileDependency(processor=ImageProcessor(
            format='JPEG', scale={'max_width': 80, 'max_height': 80}))
    ], upload_to="avatars", blank=True, null=True, validators=[validate_image])
    objects = AccountUserManager()

    def check_subscription(self):
        now = timezone.now()
        return self.subscription_end > now


# Create your models here.
