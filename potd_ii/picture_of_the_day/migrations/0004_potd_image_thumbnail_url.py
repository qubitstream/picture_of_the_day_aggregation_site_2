# -*- coding: utf-8 -*-
# Generated by Django 1.11rc1 on 2017-03-25 18:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picture_of_the_day', '0003_auto_20170325_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='potd',
            name='image_thumbnail_url',
            field=models.URLField(blank=True, editable=False, help_text='URL for the direct link to a smaller image, preferable and sufficient for importing', verbose_name='thumbnail image url'),
        ),
    ]