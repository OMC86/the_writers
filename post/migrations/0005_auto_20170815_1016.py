# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-15 10:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_auto_20170814_1346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='sub_category',
        ),
        migrations.AddField(
            model_name='post',
            name='genre',
            field=models.CharField(choices=[(b'Nonfiction', ((None, b''), (b'EX', b'Expository'), (b'AR', b'Argumentative'), (b'OP', b'Opinion'))), (b'Fiction', ((None, b''), (b'CO', b'Comedy'), (b'DR', b'Drama'), (b'HO', b'Horror'), (b'RO', b'Romance'), (b'TR', b'Tragedy'), (b'TC', b'Tragicomedy'), (b'FA', b'Fantasy'), (b'MY', b'Mythology')))], default=b'', max_length=2),
        ),
        migrations.AddField(
            model_name='post',
            name='is_entry',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='views',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='vote_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[(None, b''), (b'PO', b'Poem'), (b'SH', b'Short Story'), (b'ES', b'Essay'), (b'ME', b'Memoir'), (b'LE', b'Letter'), (b'SC', b'script'), (b'SP', b'Speech')], default=b'', max_length=2),
        ),
    ]
