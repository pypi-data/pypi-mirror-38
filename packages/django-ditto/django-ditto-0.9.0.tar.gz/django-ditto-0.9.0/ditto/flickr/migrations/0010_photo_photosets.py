# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-29 18:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flickr', '0009_photoset_fetch_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='photosets',
            field=models.ManyToManyField(to='flickr.Photoset'),
        ),
    ]
