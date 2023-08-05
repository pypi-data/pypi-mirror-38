# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-15 10:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0045_media_original_image_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='media',
            old_name='original_image_file',
            new_name='image_file',
        ),
        migrations.AlterField(
            model_name='media',
            name='image_url',
            field=models.URLField(help_text='URL of the image itself on Twitter.com'),
        ),
    ]
