# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-16 09:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0033_auto_20170914_0814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winner', to='post.Post'),
        ),
    ]
