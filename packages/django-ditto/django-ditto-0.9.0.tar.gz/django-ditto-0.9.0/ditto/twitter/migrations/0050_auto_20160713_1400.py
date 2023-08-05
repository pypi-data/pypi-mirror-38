# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-13 14:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0049_auto_20160713_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='media_type',
            field=models.CharField(choices=[('animated_gif', 'Animated GIF'), ('photo', 'Photo'), ('video', 'Video')], max_length=12),
        ),
    ]
