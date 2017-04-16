# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-16 17:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picture_of_the_day', '0005_auto_20170410_2242'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='potd',
            options={'get_latest_by': 'potd_at', 'ordering': ['-potd_at', 'source_type'], 'verbose_name': 'picture of the day', 'verbose_name_plural': 'pictures of the day'},
        ),
        migrations.RemoveField(
            model_name='potd',
            name='raw_scraping_data_image',
        ),
        migrations.AddField(
            model_name='potd',
            name='raw_scaping_data_binary_compressed',
            field=models.BinaryField(blank=True, verbose_name='lzma compressed raw scraping data for image'),
        ),
        migrations.AlterField(
            model_name='potd',
            name='copyright_info',
            field=models.TextField(blank=True, help_text='Markdown is allowed', verbose_name='copyright information'),
        ),
        migrations.AlterField(
            model_name='potd',
            name='description',
            field=models.TextField(help_text='Markdown is allowed', verbose_name='description of the picture'),
        ),
        migrations.AlterField(
            model_name='potd',
            name='image_url',
            field=models.URLField(blank=True, editable=False, help_text='URL for the direct link to the image, for the highest res available', verbose_name='image url'),
        ),
    ]