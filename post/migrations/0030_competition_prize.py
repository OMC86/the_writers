# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-08 09:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0029_auto_20170902_0414'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='prize',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]